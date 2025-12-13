# Deep Dive: Django

Django is the high-level Python Web framework that encourages rapid development and clean, pragmatic design. It is "batteries-included".

---

## 1. MVT Architecture (Model-View-Template)

Django uses **MVT**, which is slightly different from standard MVC.
*   **Model**: Database schema (SQLAlchemy uses `Session`, Django uses `Model.objects`).
*   **View**: The logic layer (Controller in MVC). Accepts request, returns response.
*   **Template**: The presentation layer (View in MVC). HTML with DTL (Django Template Language).

---

## 2. ORM Optimization (select_related vs prefetch_related)

*   `select_related()`: Uses SQL **JOIN**. Best for ForeignKey / OneToOne.
*   `prefetch_related()`: Uses **Python** to join in memory (executes 2 queries). Best for ManyToMany / Reverse ForeignKey.

```python
# JOIN in SQL
Entry.objects.select_related('blog').get(id=5)

# 1 Query for Pizzas, 1 Query for Toppings, Joined in Python
Pizza.objects.prefetch_related('toppings').all()
```

---

## 3. Middleware

Django Middleware is a framework of hooks into Django's request/response processing. It's a light, low-level "plugin" system for globally altering Django's input or output.
*   Authenticating users.
*   Session management.
*   CSRF protection.

---

## 4. Signals

Django includes a signal dispatcher which helps allow decoupled applications get notified when actions occur elsewhere in the framework.
*   `pre_save` / `post_save`: Triggered around model saving.
*   **Warning**: Signals are synchronous by default. Heavy logic in a signal slows down the save.

---

## 5. Managers and QuerySets

You can put complex query logic into custom Managers.
```python
class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.question, COUNT(c.id)
                FROM polls_poll p
                LEFT OUTER JOIN polls_choice c ON p.id = c.poll_id
                GROUP BY p.id, p.question
                ORDER BY p.date DESC""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1])
                p.num_choices = row[2]
                result_list.append(p)
        return result_list
```
