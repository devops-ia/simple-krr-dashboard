"""Table components for the simple-krr-dashboard using standard Python libraries."""

import csv
import math
from typing import Any


def convert_to_camel_case(snake_case_str: str) -> str:
    """Convert snake_case string to camelCase.

    Args:
        snake_case_str: String in snake_case format

    Returns:
        String in camelCase format
    """
    components = snake_case_str.lower().split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def read_csv_file(file_path: str) -> tuple[list[str], list[dict[str, Any]]]:
    """Read CSV file into a dictionary-based structure.

    Args:
        file_path: Path to the CSV file

    Returns:
        Tuple containing headers and rows as dictionaries

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If there's an error reading the CSV file
    """
    rows = []
    headers = []

    try:
        with open(file_path, encoding="utf-8") as file:
            reader = csv.reader(file)
            # Get header row and convert to camelCase
            raw_headers = next(reader)
            headers = [
                convert_to_camel_case(header.strip().replace(" ", "_"))
                for header in raw_headers
            ]

            for row in reader:
                row_dict = {}
                for i, header in enumerate(headers):
                    if header in ["pods", "oldPods"]:  # Pods and Old Pods columns
                        try:
                            row_dict[header] = float(row[i]) if row[i] else None
                        except ValueError:
                            row_dict[header] = None
                    else:
                        row_dict[header] = row[i]
                rows.append(row_dict)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"CSV file not found: {file_path}") from exc
    except Exception as exc:
        raise ValueError(f"Error reading CSV file: {str(exc)}") from exc

    return headers, rows


def format_status_badge(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Format the status column with HTML badges.

    Args:
        rows: List of dictionaries containing row data

    Returns:
        List of dictionaries with formatted status badges
    """
    for row in rows:
        severity = row.get("Severity", "")
        if severity == "GOOD":
            row["Severity"] = '<div class="badge badge-good">GOOD</div>'
        elif severity == "WARNING":
            row["Severity"] = '<div class="badge badge-warning">WARNING</div>'
        elif severity == "CRITICAL":
            row["Severity"] = '<div class="badge badge-critical">CRITICAL</div>'
        else:
            row["Severity"] = '<div class="badge badge-blue">OK</div>'

    return rows


def format_integer(value: Any) -> str:
    """Format value as integer if possible, otherwise return empty string.

    Args:
        value: Value to format

    Returns:
        Formatted integer as string or empty string if not possible
    """
    if value is None:
        return ""

    try:
        # NaN values
        if isinstance(value, float) and math.isnan(value):
            return ""
        return str(int(float(value)))
    except (ValueError, TypeError):
        return ""


def create_sortable_header(
    column_name: str, current_sort: str | None = None, current_ascending: bool = True
) -> str:
    """Create a sortable header with appropriate styling and data attributes.

    Args:
        column_name: Name of the column
        current_sort: Currently sorted column
        current_ascending: Whether sorting is ascending

    Returns:
        HTML string for the sortable header
    """
    sort_icon = (
        "↑"
        if current_sort == column_name and current_ascending
        else "↓" if current_sort == column_name else ""
    )
    return (
        f'<th class="sortable" data-column="{column_name}" '
        f'data-sort="{current_sort}" '
        f'data-ascending="{str(current_ascending).lower()}">'
        f"{column_name} {sort_icon}</th>"
    )


def filter_rows(
    rows: list[dict[str, Any]],
    search_term: str | None = None,
    status_filter: str | None = None,
    namespace_filter: str | None = None,
) -> list[dict[str, Any]]:
    """Filter rows based on search term, status, and namespace.

    Args:
        rows: List of dictionaries containing row data
        search_term: Term to search for in Name and Namespace
        status_filter: Filter by status
        namespace_filter: Filter by namespace

    Returns:
        Filtered list of dictionaries
    """
    filtered_rows = rows.copy()

    if search_term:
        search_term = search_term.lower()
        filtered_rows = [
            row
            for row in filtered_rows
            if (
                search_term in row.get("Name", "").lower()
                or search_term in row.get("Namespace", "").lower()
            )
        ]

    if status_filter:
        filtered_rows = [
            row for row in filtered_rows if row.get("Severity") == status_filter
        ]

    if namespace_filter:
        filtered_rows = [
            row for row in filtered_rows if row.get("Namespace") == namespace_filter
        ]

    return filtered_rows


def sort_rows(
    rows: list[dict[str, Any]],
    sort_column: str | None = None,
    sort_ascending: bool = True,
) -> list[dict[str, Any]]:
    """Sort rows by the specified column.

    Args:
        rows: List of dictionaries containing row data
        sort_column: Column to sort by
        sort_ascending: Whether to sort in ascending order

    Returns:
        Sorted list of dictionaries
    """
    if not sort_column:
        return rows

    reverse = not sort_ascending
    return sorted(
        rows,
        key=lambda x: (x.get(sort_column, "") is None, x.get(sort_column, "")),
        reverse=reverse,
    )


def generate_html_table(
    rows: list[dict[str, Any]],
    sort_column: str | None = None,
    sort_ascending: bool = True,
) -> str:
    """Generate HTML table from rows.

    Args:
        rows: List of dictionaries containing row data
        sort_column: Currently sorted column
        sort_ascending: Whether sorting is ascending

    Returns:
        HTML string for the table
    """
    display_columns = [
        "Name",
        "Namespace",
        "Pods",
        "Old Pods",
        "Type",
        "Container",
        "Severity",
        "CPU Diff",
        "CPU Requests",
        "CPU Limits",
        "Memory Diff",
        "Memory Requests",
        "Memory Limits",
    ]

    table_html = "<table class='dataframe'>"

    table_html += "<thead><tr>"
    for col in display_columns:
        table_html += create_sortable_header(col, sort_column, sort_ascending)
    table_html += "</tr></thead>"

    table_html += "<tbody>"
    for row in rows:
        table_html += "<tr>"
        for col in display_columns:
            value = row.get(col, "")
            if col in ["Pods", "Old Pods"]:
                formatted_value = format_integer(value)
            else:
                formatted_value = "" if value is None else value
            table_html += f"<td>{formatted_value}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    return table_html


def prepare_table_data(
    data: str | tuple[list[str], list[dict[str, Any]]],
    search_term: str | None = None,
    status_filter: str | None = None,
    namespace_filter: str | None = None,
    sort_column: str | None = None,
    sort_ascending: bool = True,
) -> str:
    """Prepare and filter table data.

    Args:
        data: Either a file path to a CSV file or a tuple of (headers, rows)
        search_term: Term to search for in Name and Namespace
        status_filter: Filter by status
        namespace_filter: Filter by namespace
        sort_column: Column to sort by
        sort_ascending: Whether to sort in ascending order

    Returns:
        HTML string for the table
    """
    headers, rows = data if isinstance(data, tuple) else read_csv_file(data)

    filtered_rows = filter_rows(rows, search_term, status_filter, namespace_filter)
    sorted_rows = sort_rows(filtered_rows, sort_column, sort_ascending)
    styled_rows = format_status_badge(sorted_rows)

    return generate_html_table(styled_rows, sort_column, sort_ascending)
