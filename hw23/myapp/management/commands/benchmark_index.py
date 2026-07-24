import time
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """
    Management command to measure query performance before and after dropping/recreating an index.
    """
    help = 'Benchmarks query time on Book rating field with and without index.'

    def handle(self, *args, **options) -> None:
        """
        Executes the benchmark by finding, dropping, measuring, and restoring the index.
        :param args: positional arguments
        :param options: keyword arguments
        :return: nothing
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='index' AND tbl_name='myapp_book' AND sql LIKE '%rating%';
            """)
            row = cursor.fetchone()

            if not row:
                self.stdout.write(self.style.ERROR("No index found on rating field in myapp_book table."))
                return

            index_name, create_sql = row[0], row[1]
            self.stdout.write(f"Found index: {index_name}")
            self.stdout.write(f"Creation SQL: {create_sql}")

            t0 = time.perf_counter()
            for _ in range(1000):
                cursor.execute("SELECT * FROM myapp_book WHERE rating = 4.5;")
                cursor.fetchall()
            with_index_time = time.perf_counter() - t0

            cursor.execute(f"DROP INDEX {index_name};")
            self.stdout.write(self.style.WARNING("Index dropped temporarily."))

            t0 = time.perf_counter()
            for _ in range(1000):
                cursor.execute("SELECT * FROM myapp_book WHERE rating = 4.5;")
                cursor.fetchall()
            without_index_time = time.perf_counter() - t0

            cursor.execute(create_sql)
            self.stdout.write(self.style.SUCCESS("Index successfully restored."))

            self.stdout.write("\nBenchmark Results (1000 queries):")
            self.stdout.write(f"WITHOUT index: {without_index_time:.6f} seconds")
            self.stdout.write(f"WITH index:    {with_index_time:.6f} seconds")
            
            speedup = (without_index_time / with_index_time) if with_index_time > 0 else 0
            self.stdout.write(f"Speedup:       {speedup:.1f}x")
