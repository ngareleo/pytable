from pytable import Table, Col

if __name__ == "__main__":
    Table.columns(
        Col(name="first_name", label="First name"),
        Col(name="id", label="ID"),
        Col(name="dob", label="D.O.Birth"),
    ).body(
        [
            ["Bruce Wayne", "23232", "12/08/1988"],
            ["Bruce Wayne", "23232", "12/08/1988"],
            ["Bruce Wayne", "23232", "12/08/1988"],
        ]
    ).draw()  # Should draw the table

    Table.body(
        [
            ["First Name", "ID", "DOB"],
            ["Bruce Wayne", "23232", "12/08/1988"],
            ["Princess Diana of Themyscira", "47568", "12/08/1801"],
            ["Clark Kent", "23232", "unknown"],
        ]
    ).draw()  # Should derive the header from the first row

    Table.body(
        [
            ["Bruce Wayne", "23232", "12/08/1988"],
            ["Bruce Wayne", "23232", "12/08/1988"],
            ["Bruce Wayne", "23232", "12/08/1988"],
        ]
    ).config(
        headerless=True
    ).draw()  # Should draw a table without a header
