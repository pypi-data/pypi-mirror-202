# this plug point defines all the possible access patterns and write
# patterns for the report status object
# the plugin that implements this plug point can use this information
# to define the appropriate storage and efficient ways to provide the
# handle data with that storage


class InitiateReportGenerationPlugPoint:
    def __init__(self):
        pass

    def produce_msg_report_generate(self, report_id, account_number, date):
        """
        this method produces a message to generate the account analysis report.
        :param report_id:
        :param account_number:
        :param date:
        :return:
        """
        # TODO get this from karyastala
        pass
