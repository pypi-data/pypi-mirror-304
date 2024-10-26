from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render
from chart.models import Chart
from django.core.exceptions import FieldDoesNotExist

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'view_chart')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart/<int:chart_id>/', self.admin_site.admin_view(self.chart_view), name='chart_view'),
        ]
        return custom_urls + urls

    def view_chart(self, obj):
        url = reverse('admin:chart_view', args=[obj.id])
        return format_html('<a href="{}">View Chart</a>', url)

    def chart_view(self, request, chart_id):
        chart = Chart.objects.get(id=chart_id)
        model = chart.model_name.model_class()
        model_field = chart.model_field

        # Try to select a date field, with 'date_joined' or 'created_at'
        date_field = None
        try:
            model._meta.get_field('date_joined')
            date_field = 'date_joined'
        except FieldDoesNotExist:
            try:
                model._meta.get_field('created_at')
                date_field = 'created_at'
            except FieldDoesNotExist:
                return render(request, 'admin/chart_template.html', {
                    'chart': chart,
                    'model_name': chart.model_name.name,
                    'model_field': model_field,
                    'error': 'Neither "date_joined" nor "created_at" exists in the model.',
                })

        # Annotate data by the chosen date field, summing counts per date
        data = model.objects.values(date_field).annotate(count=Count('id')).order_by(date_field)

        # Aggregate counts for each date
        aggregated_data = {}
        for entry in data:
            date_str = entry[date_field].strftime('%Y-%m-%d')
            if date_str in aggregated_data:
                aggregated_data[date_str] += entry['count']
            else:
                aggregated_data[date_str] = entry['count']

        # Prepare data for the chart
        dates = list(aggregated_data.keys())
        counts = list(aggregated_data.values())

        datasets = []
        if model_field:
            fields = [field.strip() for field in model_field.split(',')]
            for field in fields:
                total_sum_data = model.objects.values(date_field).annotate(total_sum=Sum(field)).order_by(date_field)

                total_sum_values = []
                for date_str in dates:
                    total_sum_entry = next((item['total_sum'] for item in total_sum_data if item[date_field].strftime('%Y-%m-%d') == date_str), 0)
                    total_sum_values.append(total_sum_entry)

                datasets.append({
                    'label': f'Total {field}',
                    'data': total_sum_values,
                    'borderColor': self.get_color_for_dataset(len(datasets)),
                    'borderWidth': 2,
                    'fill': False,
                })

        context = {
            'chart': chart,
            'model_name': chart.model_name.name,
            'model_field': model_field,
            'dates': dates,
            'counts': counts,
            'datasets': datasets,
        }
        return render(request, 'admin/chart_template.html', context)


    def get_color_for_dataset(self, index):
        # List of colors for datasets
        colors = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
        ]
        return colors[index % len(colors)]  # Cycle through colors
