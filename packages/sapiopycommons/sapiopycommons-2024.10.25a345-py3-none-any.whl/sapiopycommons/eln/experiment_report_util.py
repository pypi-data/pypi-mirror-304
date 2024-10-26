from sapiopylib.rest.ELNService import ElnManager
from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldType
from sapiopylib.rest.pojo.eln.ElnExperiment import ElnExperiment, ElnExperimentQueryCriteria
from sapiopylib.rest.utils.recordmodel.RecordModelWrapper import WrappedType

from sapiopycommons.customreport.custom_report_builder import CustomReportBuilder
from sapiopycommons.customreport.term_builder import TermBuilder
from sapiopycommons.datatype.pseudo_data_types import EnbEntryOptionsPseudoDef, NotebookExperimentOptionPseudoDef, \
    NotebookExperimentPseudoDef, ExperimentEntryRecordPseudoDef, EnbEntryPseudoDef
from sapiopycommons.general.aliases import SapioRecord, UserIdentifier, AliasUtil, FieldValue, \
    ExperimentEntryIdentifier, ExperimentIdentifier
from sapiopycommons.general.custom_report_util import CustomReportUtil
from sapiopycommons.recordmodel.record_handler import RecordHandler


# FR-46908 - Provide a utility class that holds experiment related custom reports e.g. getting all the experiments
# that given records were used in or getting all records of a datatype used in given experiments.
class ExperimentReportUtil:
    @staticmethod
    def map_records_to_experiment_ids(context: UserIdentifier, records: list[SapioRecord]) \
            -> dict[SapioRecord, list[int]]:
        """
        Return a dictionary mapping each record to a list of ids of experiments that they were used in.
        If a record wasn't used in any experiments then it will be mapped to an empty list.

        :param context: The current webhook context or a user object to send requests from.
        :param records: A list of records of the same data type.
        :return: A dictionary mapping each record to a list of ids of each experiment it was used in.
        """
        if not records:
            return {}

        user: SapioUser = AliasUtil.to_sapio_user(context)
        data_type_name: str = AliasUtil.to_singular_data_type_name(records)

        record_ids = [record.record_id for record in records]
        rows = ExperimentReportUtil.__get_record_experiment_relation_rows(user, data_type_name, record_ids=record_ids)

        id_to_record: dict[int, SapioRecord] = RecordHandler.map_by_id(records)
        record_to_exps: dict[SapioRecord, set[int]] = {record: set() for record in records}
        for row in rows:
            record_id: int = row["RecordId"]
            exp_id: int = row[NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME.field_name]
            record = id_to_record[record_id]
            record_to_exps[record].add(exp_id)

        return {record: list(exps) for record, exps in record_to_exps.items()}

    @staticmethod
    def map_experiments_to_records_of_type(context: UserIdentifier, exp_ids: list[ExperimentIdentifier],
                                           wrapper_type: type[WrappedType]) -> dict[int, list[WrappedType]]:
        """
        Return a dictionary mapping each experiment id to a list of records of the given type that were used in each
        experiment. If an experiment didn't use any records of the given type then it will be mapped to an empty list.

        :param context: The current webhook context or a user object to send requests from.
        :param exp_ids: A list of experiment identifiers.
        :param wrapper_type: The record model wrapper to use, corresponds to which data type we will query for.
        :return: A dictionary mapping each experiment id to a list of records of the given type that were used in that
            experiment.
        """
        if not exp_ids:
            return {}

        user = AliasUtil.to_sapio_user(context)
        record_handler = RecordHandler(user)
        data_type_name: str = wrapper_type.get_wrapper_data_type_name()

        exp_ids: list[int] = AliasUtil.to_notebook_ids(exp_ids)
        rows = ExperimentReportUtil.__get_record_experiment_relation_rows(user, data_type_name, exp_ids=exp_ids)
        record_ids: set[int] = {row["RecordId"] for row in rows}
        records = record_handler.query_models_by_id(wrapper_type, record_ids)

        id_to_record: dict[int, WrappedType] = RecordHandler.map_by_id(records)
        exp_to_records: dict[int, set[SapioRecord]] = {exp: set() for exp in exp_ids}
        for row in rows:
            record_id: int = row["RecordId"]
            exp_id: int = row[NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME.field_name]
            record = id_to_record[record_id]
            exp_to_records[exp_id].add(record)

        return {exp: list(records) for exp, records in exp_to_records.items()}

    @staticmethod
    def get_experiment_options(context: UserIdentifier, experiments: list[ExperimentIdentifier]) \
            -> dict[int, dict[str, str]]:
        """
        Run a custom report to retrieve the experiment options for all the provided experiments. Effectively a batched
        version of the get_notebook_experiment_options function of ElnManager.

        :param context: The current webhook context or a user object to send requests from.
        :param experiments: The experiment identifiers to retrieve the experiment options for.
        :return: A dictionary mapping the notebook experiment ID to the options for that experiment.
        """
        exp_ids: list[int] = AliasUtil.to_notebook_ids(experiments)

        report_builder = CustomReportBuilder(NotebookExperimentOptionPseudoDef.DATA_TYPE_NAME)
        root = TermBuilder.is_term(NotebookExperimentOptionPseudoDef.DATA_TYPE_NAME,
                                   NotebookExperimentOptionPseudoDef.EXPERIMENT_ID__FIELD_NAME,
                                   exp_ids)
        report_builder.set_root_term(root)
        report_builder.add_column(NotebookExperimentOptionPseudoDef.EXPERIMENT_ID__FIELD_NAME)
        report_builder.add_column(NotebookExperimentOptionPseudoDef.OPTION_KEY__FIELD_NAME)
        report_builder.add_column(NotebookExperimentOptionPseudoDef.OPTION_VALUE__FIELD_NAME)
        report = report_builder.build_report_criteria()

        # Ensure that each experiment appears in the dictionary, even if it has no experiment options.
        options: dict[int, dict[str, str]] = {x: {} for x in exp_ids}
        results: list[dict[str, FieldValue]] = CustomReportUtil.run_custom_report(context, report)
        for row in results:
            exp_id: int = row[NotebookExperimentOptionPseudoDef.EXPERIMENT_ID__FIELD_NAME.field_name]
            key: str = row[NotebookExperimentOptionPseudoDef.OPTION_KEY__FIELD_NAME.field_name]
            value: str = row[NotebookExperimentOptionPseudoDef.OPTION_VALUE__FIELD_NAME.field_name]
            options[exp_id][key] = value
        return options

    @staticmethod
    def get_experiment_entry_options(context: UserIdentifier, entries: list[ExperimentEntryIdentifier]) \
            -> dict[int, dict[str, str]]:
        """
        Run a custom report to retrieve the entry options for all the provided entries. Effectively a batched
        version of the get_experiment_entry_options function of ElnManager.

        :param context: The current webhook context or a user object to send requests from.
        :param entries: The experiment entry identifiers to retrieve the entry options for.
        :return: A dictionary mapping the entry ID to the options for that entry.
        """
        entries: list[int] = AliasUtil.to_entry_ids(entries)
        report_builder = CustomReportBuilder(EnbEntryOptionsPseudoDef.DATA_TYPE_NAME)
        root = TermBuilder.is_term(EnbEntryOptionsPseudoDef.DATA_TYPE_NAME,
                                   EnbEntryOptionsPseudoDef.ENTRY_ID__FIELD_NAME,
                                   entries)
        report_builder.set_root_term(root)
        report_builder.add_column(EnbEntryOptionsPseudoDef.ENTRY_ID__FIELD_NAME)
        report_builder.add_column(EnbEntryOptionsPseudoDef.ENTRY_OPTION_KEY__FIELD_NAME)
        report_builder.add_column(EnbEntryOptionsPseudoDef.ENTRY_OPTION_VALUE__FIELD_NAME)
        report = report_builder.build_report_criteria()

        # Ensure that each entry appears in the dictionary, even if it has no entry options.
        options: dict[int, dict[str, str]] = {x: {} for x in entries}
        results: list[dict[str, FieldValue]] = CustomReportUtil.run_custom_report(context, report)
        for row in results:
            entry_id: int = row[EnbEntryOptionsPseudoDef.ENTRY_ID__FIELD_NAME.field_name]
            key: str = row[EnbEntryOptionsPseudoDef.ENTRY_OPTION_KEY__FIELD_NAME.field_name]
            value: str = row[EnbEntryOptionsPseudoDef.ENTRY_OPTION_VALUE__FIELD_NAME.field_name]
            options[entry_id][key] = value
        return options

    @staticmethod
    def get_experiments_by_name(context: UserIdentifier, name: str) -> list[ElnExperiment]:
        """
        Run a custom report that retrieves every experiment in the system with a given name.

        :param context: The current webhook context or a user object to send requests from.
        :param name: The name of the experiment to query for.
        :return: A list of every experiment in the system with a name that matches the input.
        """
        return ExperimentReportUtil.get_experiments_by_names(context, [name])[name]

    @staticmethod
    def get_experiments_by_names(context: UserIdentifier, names: list[str]) -> dict[str, list[ElnExperiment]]:
        """
        Run a custom report that retrieves every experiment in the system with a name from a list of names.

        :param context: The current webhook context or a user object to send requests from.
        :param names: The names of the experiment to query for.
        :return: A dictionary mapping the experiment name to a list of every experiment in the system with that name.
        """
        user = AliasUtil.to_sapio_user(context)

        report_builder = CustomReportBuilder(NotebookExperimentPseudoDef.DATA_TYPE_NAME)
        report_builder.add_column(NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME)
        root = TermBuilder.is_term(NotebookExperimentPseudoDef.DATA_TYPE_NAME,
                                   NotebookExperimentPseudoDef.EXPERIMENT_NAME__FIELD_NAME,
                                   names)
        report_builder.set_root_term(root)

        # Ensure that each entry appears in the dictionary, even if it has no experiments.
        ret_val: dict[str, list[ElnExperiment]] = {x: [] for x in names}

        exp_ids: list[int] = []
        for row in CustomReportUtil.run_custom_report(user, report_builder.build_report_criteria()):
            exp_ids.append(row[NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME.field_name])
        if not exp_ids:
            return ret_val

        criteria = ElnExperimentQueryCriteria(notebook_experiment_id_white_list=exp_ids)
        experiments: list[ElnExperiment] = ElnManager(user).get_eln_experiment_by_criteria(criteria)
        for experiment in experiments:
            ret_val.get(experiment.notebook_experiment_name).append(experiment)
        return ret_val

    @staticmethod
    def __get_record_experiment_relation_rows(user: SapioUser, data_type_name: str, record_ids: list[int] | None = None,
                                              exp_ids: list[int] | None = None) -> list[dict[str, int]]:
        """
        Return a list of dicts mapping \"RECORDID\" to the record id and \"EXPERIMENTID\" to the experiment id.
        At least one of record_ids and exp_ids should be provided.
        """
        assert (record_ids or exp_ids)

        if record_ids:
            records_term = TermBuilder.is_term(data_type_name, "RecordId", record_ids)
        else:
            # Get all records of the given type
            records_term = TermBuilder.all_records_term(data_type_name)

        if exp_ids:
            exp_term = TermBuilder.is_term(NotebookExperimentPseudoDef.DATA_TYPE_NAME,
                                           NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME,
                                           exp_ids)
        else:
            # Get all experiments
            exp_term = TermBuilder.gte_term(NotebookExperimentPseudoDef.DATA_TYPE_NAME,
                                            NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME,
                                            0)

        root_term = TermBuilder.and_terms(records_term, exp_term)

        # Join records on the experiment entry records that correspond to them.
        records_entry_join = TermBuilder.compare_is_term(ExperimentEntryRecordPseudoDef.DATA_TYPE_NAME,
                                                         ExperimentEntryRecordPseudoDef.RECORD_ID__FIELD_NAME,
                                                         data_type_name,
                                                         "RecordId")
        # Join entry records on the experiment entries they are in.
        experiment_entry_enb_entry_join = TermBuilder.compare_is_term(EnbEntryPseudoDef.DATA_TYPE_NAME,
                                                                      EnbEntryPseudoDef.ENTRY_ID__FIELD_NAME,
                                                                      ExperimentEntryRecordPseudoDef.DATA_TYPE_NAME,
                                                                      ExperimentEntryRecordPseudoDef.ENTRY_ID__FIELD_NAME)
        # Join entries on the experiments they are in.
        enb_entry_experiment_join = TermBuilder.compare_is_term(NotebookExperimentPseudoDef.DATA_TYPE_NAME,
                                                                NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME,
                                                                EnbEntryPseudoDef.DATA_TYPE_NAME,
                                                                EnbEntryPseudoDef.EXPERIMENT_ID__FIELD_NAME)

        report_builder = CustomReportBuilder(data_type_name)
        report_builder.set_root_term(root_term)
        report_builder.add_column("RecordId", FieldType.LONG)
        report_builder.add_column(NotebookExperimentPseudoDef.EXPERIMENT_ID__FIELD_NAME,
                                  data_type=NotebookExperimentPseudoDef.DATA_TYPE_NAME)
        report_builder.add_join(records_entry_join)
        report_builder.add_join(experiment_entry_enb_entry_join)
        report_builder.add_join(enb_entry_experiment_join)
        return CustomReportUtil.run_custom_report(user, report_builder.build_report_criteria())
