import voyageai
import os
from math import sqrt
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("VOYAGYE_SECRET_KEY")

vo = voyageai.Client(api_key=API_KEY)

query_text = "Что делать, если купленная вещь не подошла?"  # ни одного общего слова с "правильным" документом ниже

documents = [
    "Возврат товара возможен в течение 14 дней после покупки",  # правильный ответ, но НИ ОДНОГО общего слова с вопросом
    "Обмен товара на другой размер возможен при наличии чека",  # лексически близко ("товара", "возможен"), но другая процедура (обмен, не возврат)
    "Возврат денег за оказанную услугу занимает 5-10 рабочих дней",  # содержит слово "возврат" — лексический дубль, но это про услуги, не про товар
]

similarity_list_with_type = []
similarity_list_without_type = []

result_doc_with_type = vo.embed(documents, model = "voyage-4-nano", input_type = "document")
result_query_with_type = vo.embed([query_text], model = "voyage-4-nano", input_type = "query")
result_doc_without_type = vo.embed(documents, model = "voyage-4-nano")
result_query_without_type = vo.embed([query_text], model = "voyage-4-nano")

def cosine_similarity(result_doc, result_query, index):
    dot_product = sum(vec_a * vec_b for vec_a, vec_b in zip(result_doc.embeddings[index], result_query.embeddings[0]))
    len_vec_a = sqrt(sum(vec_a ** 2 for vec_a in result_doc.embeddings[index]))
    len_vec_b = sqrt(sum(vec_b ** 2 for vec_b in result_query.embeddings[0]))
    
    return dot_product / (len_vec_a * len_vec_b)

for index, document in enumerate(documents):
    similarity = cosine_similarity(result_doc_with_type, result_query_with_type, index)
    similarity_list_with_type.append(similarity)
    
for index, document in enumerate(documents):
    similarity = cosine_similarity(result_doc_without_type, result_query_without_type, index)
    similarity_list_without_type.append(similarity)
    
pairs_with_type = list(zip(similarity_list_with_type, documents))
sorted_pairs_with = sorted(pairs_with_type, reverse=True)    
pairs_without_type = list(zip(similarity_list_without_type, documents))
sorted_pairs_without = sorted(pairs_without_type, reverse=True)

gap_with = (sorted_pairs_with[0][0] - sorted_pairs_with[1][0])/sorted_pairs_with[0][0]
gap_without = (sorted_pairs_without[0][0] - sorted_pairs_without[1][0])/sorted_pairs_without[0][0]
print(sorted_pairs_with)
print(sorted_pairs_without)
print(gap_with, gap_without)






