from collections import Counter
from job.models import Vacancy
from recruitment_cp.models import ParameterKeyword
import math

def get_vacancy_in_sublists(objects_per_list=5) -> list:
    objects = list(Vacancy.objects.all().order_by('?')[:10])
    
    total_objects = len(objects)
    
    number_of_lists = math.ceil(total_objects / objects_per_list)
    
    sublists = [
        objects[i * objects_per_list:(i + 1) * objects_per_list]
        for i in range(number_of_lists)
    ]

    return sublists

def get_trending_keywords():
    vacancies = Vacancy.objects.all()
    all_keywords = []

    for vacancy in vacancies:
        if vacancy.keywords:
            for keyword in vacancy.keywords:
                if isinstance(keyword, list):
                    all_keywords.extend(keyword)
                else:
                    all_keywords.append(keyword)
    
    keyword_counter = Counter(all_keywords)

    # En çok kullanılan 5 keyword
    most_common_keywords = keyword_counter.most_common(5)

    # Keyword ID'leri yerine isimlerini almak isterseniz
    most_common_keyword_ids = [keyword_id for keyword_id, count in most_common_keywords]
    most_common_keyword_names = ParameterKeyword.objects.filter(id__in=most_common_keyword_ids).values_list('name', flat=True)

    return most_common_keyword_names