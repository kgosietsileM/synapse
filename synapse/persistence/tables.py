# -*- coding: utf-8 -*-

from collections import namedtuple


_select_where_clause = "SELECT %s FROM %s WHERE %s"
_select_clause = "SELECT %s FROM %s"
_insert_clause = "INSERT OR REPLACE INTO %s (%s) VALUES (%s)"


class Table(object):
    """ A base class used to store information about a particular table.
    """

    table_name = None
    """ str: The name of the table """

    fields = None
    """ list: The field names """

    EntryType = None
    """ Type: A tuple type used to decode the results """

    CoumnNames = None
    """ collections.namedtuple: A trivial convenience mapping from
            column names -> column names.
    """

    @classmethod
    def select_statement(clz, where_clause=None):
        """
        Args:
            where_clause (str): The WHERE clause to use.

        Returns:
            str: An SQL statement to select rows from the table with the given
            WHERE clause.
        """
        if where_clause:
            return _select_where_clause % (
                    ", ".join(clz.fields),
                    clz.table_name,
                    where_clause
                )
        else:
            return _select_clause % (
                    ", ".join(clz.fields),
                    clz.table_name,
                )

    @classmethod
    def insert_statement(clz):
        return _insert_clause % (
                clz.table_name,
                ", ".join(clz.fields),
                ", ".join(["?"] * len(clz.fields)),
            )

    @classmethod
    def decode_results(clz, results):
        """ Given an iterable of tuples, return a list of `EntryType`
        Args:
            results (list): The results list to convert to `EntryType`

        Returns:
            list: A list of `EntryType`
        """
        return [clz.EntryType(*row) for row in results]

    @staticmethod
    def generate_where(*field_names):
        return " AND ".join(["%s = ?" % f for f in field_names])

    @classmethod
    def get_fields_string(clz, prefix=None):
        if prefix:
            to_join = ("%s.%s" % (prefix, f) for f in clz.fields)
        else:
            to_join = clz.fields

        return ", ".join(to_join)


class ReceivedTransactionsTable(Table):
    table_name = "received_transactions"

    fields = [
        "transaction_id",
        "origin",
        "ts",
        "response_code",
        "response_json",
        "has_been_referenced",
    ]

    EntryType = namedtuple("ReceivedTransactionsEntry", fields)

    CoumnNames = EntryType(*fields)


class SentTransactions(Table):
    table_name = "sent_transactions"

    fields = [
        "id",
        "transaction_id",
        "destination",
        "ts",
        "response_code",
        "response_json",
    ]

    EntryType = namedtuple("SentTransactionsEntry", fields)

    CoumnNames = EntryType(*fields)


class TransactionsToPduTable(Table):
    table_name = "transaction_id_to_pdu"

    fields = [
        "transaction_id",
        "destination",
        "pdu_id",
        "pdu_origin",
    ]

    EntryType = namedtuple("TransactionsToPduEntry", fields)

    CoumnNames = EntryType(*fields)


class PdusTable(Table):
    table_name = "pdus"

    fields = [
        "pdu_id",
        "origin",
        "context",
        "pdu_type",
        "ts",
        "version",
        "content_json",
        "unrecognized_keys",
        "outlier",
        "have_processed",
    ]

    EntryType = namedtuple("PdusEntry", fields)

    CoumnNames = EntryType(*fields)


class StatePdusTable(Table):
    table_name = "state_pdus"

    fields = [
        "pdu_id",
        "origin",
        "context",
        "pdu_type",
        "state_key",
        "power_level",
        "prev_state_id",
        "prev_state_origin",
    ]

    EntryType = namedtuple("StatePdusEntry", fields)

    CoumnNames = EntryType(*fields)


class CurrentStateTable(Table):
    table_name = "current_state"

    fields = [
        "pdu_id",
        "origin",
        "context",
        "pdu_type",
        "state_key",
    ]

    EntryType = namedtuple("CurrentStateEntry", fields)

    CoumnNames = EntryType(*fields)


class PduDestinationsTable(Table):
    table_name = "pdu_destinations"

    fields = [
        "pdu_id",
        "origin",
        "destination",
        "delivered_ts",
    ]

    EntryType = namedtuple("PduDestinationsEntry", fields)

    CoumnNames = EntryType(*fields)


class PduEdgesTable(Table):
    table_name = "pdu_edges"

    fields = [
        "pdu_id",
        "origin",
        "prev_pdu_id",
        "prev_origin",
        "context"
    ]

    EntryType = namedtuple("PduEdgesEntry", fields)

    CoumnNames = EntryType(*fields)


class PduForwardExtremetiesTable(Table):
    table_name = "pdu_forward_extremeties"

    fields = [
        "pdu_id",
        "origin",
        "context",
    ]

    EntryType = namedtuple("PduForwardExtremetiesEntry", fields)

    CoumnNames = EntryType(*fields)


class PduBackwardExtremetiesTable(Table):
    table_name = "pdu_backward_extremeties"

    fields = [
        "pdu_id",
        "origin",
        "context",
    ]

    EntryType = namedtuple("PduBackwardExtremetiesEntry", fields)

    CoumnNames = EntryType(*fields)


class ContextDepthTable(Table):
    table_name = "context_depth"

    fields = [
        "context",
        "min_depth",
    ]

    EntryType = namedtuple("ContextDepthEntry", fields)

    CoumnNames = EntryType(*fields)