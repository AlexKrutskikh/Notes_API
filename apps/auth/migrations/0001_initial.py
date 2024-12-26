# Generated by Django 5.1.1 on 2024-12-26 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="SmsCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=6)),
                ("sent_time", models.DateTimeField()),
                ("phone", models.CharField(max_length=50)),
                ("ip", models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("auth_provider", models.CharField(default="Twilio", max_length=50)),
                ("registration_time", models.DateTimeField(auto_now_add=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ("first_name", models.CharField(blank=True, max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                ("username", models.CharField(blank=True, max_length=100)),
                ("phone", models.CharField(blank=True, max_length=50, null=True, unique=True)),
                (
                    "type",
                    models.CharField(choices=[("CL", "Client"), ("SP", "Specialist")], default="CL", max_length=2),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PR", "Profile_prefill"),
                            ("SS", "Status_select"),
                            ("VC", "Vetbook_creation"),
                            ("SF", "Specialist_info_fill"),
                            ("SV", "Specialist_verification"),
                            ("DONE", "Done"),
                        ],
                        default="SS",
                        max_length=6,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
