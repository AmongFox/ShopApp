import json
import os

from django.conf import settings
from django.contrib import admin, messages
from django.core import serializers
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from .models import ProductModel


class ProductAdmin(admin.ModelAdmin):
    model = ProductModel
    actions = [
        "export_as_json",
        "import_from_json",
    ]
    list_display = (
        "name",
        "description",
        "price",
        "discount",
        "quantity",
        "created_date",
        "created_by",
        "archived",
        "preview",
    )
    list_filter = ("created_date", "created_by", "archived")
    search_fields = ("name", "description", "created_by__username")
    ordering = ("name", "price", "discount", "quantity", "created_date")

    fieldsets = (
        (None, {"fields": ("name", "description")}),
        ("Цена и наличие", {"fields": ("price", "discount", "quantity")}),
        ("Статус и изображение", {"fields": ("archived", "preview")}),
        ("Владелец", {"fields": ("created_by",)}),
    )

    # Добавляем кастомные URL для импорта
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-json/", self.import_json, name="import_json"),
        ]
        return custom_urls + urls

    def export_as_json(self, request, queryset):
        data = serializers.serialize("json", queryset)
        response = HttpResponse(data, content_type="application/json")
        response["Content-Disposition"] = "attachment; filename=export.json"
        return response

    export_as_json.short_description = "Экспортировать выбранные объекты в JSON"

    def import_from_json(self, request, queryset):
        return HttpResponseRedirect("import-json/")

    import_from_json.short_description = "Импортировать данные из JSON"

    def import_json(self, request):
        if request.method == "POST" and request.FILES.get("json_file"):
            json_file = request.FILES["json_file"]
            try:
                # Читаем и декодируем файл
                file_content = json_file.read().decode("utf-8")
                data = json.loads(file_content)

                if not isinstance(data, list):
                    raise ValueError("JSON должен содержать массив объектов")

                imported_count = 0

                for item in data:
                    try:
                        # Формат Django serializers
                        if "model" in item and "fields" in item:
                            if item["model"] != "shop_app.productmodel":
                                continue

                            fields = item["fields"]
                            # Преобразуем поля под нашу модель
                            product_data = {
                                "name": fields.get("name", ""),
                                "description": fields.get("description", ""),
                                "price": fields.get("price", 0),
                                "discount": fields.get("discount", 0),
                                "quantity": fields.get("quantity", 0),
                                "archived": fields.get("archived", False),
                                "created_by_id": fields.get(
                                    "created_by", request.user.id
                                ),
                            }
                            preview_path = fields.get("preview", "")
                        else:
                            # Простой JSON формат
                            product_data = {
                                "name": item.get("name", ""),
                                "description": item.get("description", ""),
                                "price": item.get("price", 0),
                                "discount": item.get("discount", 0),
                                "quantity": item.get("quantity", 0),
                                "archived": item.get("archived", False),
                                "created_by_id": item.get(
                                    "created_by", request.user.id
                                ),
                            }
                            preview_path = item.get("preview", "")

                        # Создаем продукт (сначала без изображения)
                        product = ProductModel.objects.create(**product_data)

                        # Обрабатываем изображение, если путь указан
                        if preview_path:
                            try:
                                # Полный путь к файлу в медиа-папке
                                full_path = os.path.join(
                                    settings.MEDIA_ROOT, preview_path
                                )

                                if os.path.exists(full_path):
                                    # Открываем файл и создаем объект File
                                    with open(full_path, "rb") as f:
                                        file_name = os.path.basename(preview_path)
                                        django_file = File(f, name=file_name)
                                        product.preview.save(
                                            file_name, django_file, save=True
                                        )
                                else:
                                    raise FileNotFoundError(
                                        f"Файл изображения не найден: {full_path}"
                                    )
                            except Exception as e:
                                # Если не удалось загрузить изображение, удаляем продукт
                                product.delete()
                                raise Exception(
                                    f"Ошибка загрузки изображения: {str(e)}"
                                )

                        imported_count += 1

                    except Exception as e:
                        self.message_user(
                            request,
                            f"Ошибка при импорте объекта: {str(e)}",
                            messages.WARNING,
                        )
                        continue

                self.message_user(
                    request,
                    f"Успешно импортировано {imported_count} из {len(data)} объектов",
                    messages.SUCCESS,
                )

            except Exception as e:
                self.message_user(request, f"Ошибка импорта: {str(e)}", messages.ERROR)

            return HttpResponseRedirect("../")

        # Отображение формы импорта
        context = self.admin_site.each_context(request)
        context["opts"] = self.model._meta
        context["title"] = "Импорт продуктов из JSON"
        return render(request, "admin/shop_app/json-import.html", context)


# Регистрируем модель только один раз
admin.site.register(ProductModel, ProductAdmin)
