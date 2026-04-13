from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0006_quiz_ranking_dojo"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuizQuestionProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_key", models.CharField(db_index=True, max_length=128)),
                ("times_seen", models.PositiveIntegerField(default=0)),
                ("times_correct", models.PositiveIntegerField(default=0)),
                ("first_correct_at", models.DateTimeField(blank=True, null=True)),
                ("data_atualizacao", models.DateTimeField(auto_now=True)),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_question_progress", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("usuario", "question_key")},
            },
        ),
        migrations.AddIndex(
            model_name="quizquestionprogress",
            index=models.Index(fields=["usuario", "question_key"], name="qqp_user_key_idx"),
        ),
        migrations.CreateModel(
            name="QuizAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nivel_quiz", models.PositiveIntegerField(default=1)),
                ("total_perguntas", models.PositiveIntegerField(default=8)),
                ("question_keys", models.JSONField(default=list)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("elapsed_seconds", models.PositiveIntegerField(blank=True, null=True)),
                ("correct_count", models.PositiveIntegerField(default=0)),
                ("xp_awarded", models.PositiveIntegerField(default=0)),
                ("bonus_time_xp", models.PositiveIntegerField(default=0)),
                ("suspicious", models.BooleanField(default=False)),
                ("suspicious_reason", models.CharField(blank=True, default="", max_length=200)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_attempts", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name="quizattempt",
            index=models.Index(fields=["usuario", "started_at"], name="qattempt_user_start_idx"),
        ),
        migrations.AddIndex(
            model_name="quizattempt",
            index=models.Index(fields=["usuario", "nivel_quiz"], name="qattempt_user_level_idx"),
        ),
    ]

