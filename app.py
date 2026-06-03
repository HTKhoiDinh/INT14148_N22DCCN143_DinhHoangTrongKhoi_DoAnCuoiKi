from flask import Flask, render_template, request

from middleware.detector import analyze_sql
from middleware.parser import extract_id
from middleware.router import get_fragment
from middleware.permission import allowed
from middleware.executor import execute_query
from middleware.logger import write_log


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():

    user = request.form.get("user", "").strip().lower()
    sql = request.form.get("sql", "").strip()

    # 1. Security policy check
    analysis = analyze_sql(sql)

    if not analysis["allowed"]:

        write_log(
            user=user,
            sql=sql,
            result="BLOCKED_MALICIOUS",
            reason=analysis["reason"]
        )

        return render_template(
            "result.html",
            status="BLOCKED",
            color="danger",
            message="SQL Injection or forbidden SQL pattern detected",
            reason=analysis["reason"],
            user=user,
            sql=sql,
            site=None,
            employee=None
        )

    # 2. Parse Employee ID from SQL
    emp_id = extract_id(sql)

    if emp_id is None:

        write_log(
            user=user,
            sql=sql,
            result="REJECTED_UNSUPPORTED_QUERY",
            reason="CANNOT_EXTRACT_EMPLOYEE_ID"
        )

        return render_template(
            "result.html",
            status="REJECTED",
            color="warning",
            message="Unsupported SQL query format",
            reason="Query must contain condition like WHERE ID=100",
            user=user,
            sql=sql,
            site=None,
            employee=None
        )

    # 3. Find distributed fragment from config
    fragment = get_fragment("Employee", emp_id)

    if fragment is None:

        write_log(
            user=user,
            sql=sql,
            result="REJECTED_NO_FRAGMENT",
            reason="NO_FRAGMENT_FOUND"
        )

        return render_template(
            "result.html",
            status="REJECTED",
            color="warning",
            message="No distributed fragment found for this query",
            reason="Employee ID does not belong to any configured fragment",
            user=user,
            sql=sql,
            site=None,
            employee=None
        )

    # 4. User-fragment access control
    if not allowed(user, fragment):

        write_log(
            user=user,
            sql=sql,
            result="ACCESS_DENIED",
            reason="UNAUTHORIZED_FRAGMENT_ACCESS",
            site=fragment["site"]
        )

        return render_template(
            "result.html",
            status="ACCESS DENIED",
            color="danger",
            message="Unauthorized fragment access",
            reason=f"User '{user}' is not allowed to access {fragment['site']}",
            user=user,
            sql=sql,
            site=fragment,
            employee=None
        )

    # 5. Execute safe parameterized query
    employee = execute_query(fragment, emp_id)

    if employee is None:

        write_log(
            user=user,
            sql=sql,
            result="NOT_FOUND",
            reason="EMPLOYEE_NOT_FOUND",
            site=fragment["site"]
        )

        return render_template(
            "result.html",
            status="NOT FOUND",
            color="secondary",
            message="Employee not found",
            reason="No record found in selected distributed fragment",
            user=user,
            sql=sql,
            site=fragment,
            employee=None
        )

    # 6. Success
    write_log(
        user=user,
        sql=sql,
        result="ALLOWED",
        reason="QUERY_EXECUTED_SUCCESSFULLY",
        site=fragment["site"]
    )

    return render_template(
        "result.html",
        status="ALLOWED",
        color="success",
        message="Query passed all Query Guard checks",
        reason="Query was routed and executed on the correct distributed site",
        user=user,
        sql=sql,
        site=fragment,
        employee=employee
    )


if __name__ == "__main__":
    app.run(debug=True)