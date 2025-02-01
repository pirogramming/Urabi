from django.shortcuts import render 
from django.http import JsonResponse 
from openai import OpenAI
import os
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_completion(prompt): 
	print(prompt) 
	query = client.chat.completions.create( 
		model="gpt-3.5-turbo",
		messages=[
        	{'role':'user','content': prompt}
    	], 
		max_tokens=1024, 
		n=1, 
		stop=None, 
		temperature=0.5, 
	) 
	response = query.choices[0].message.content
	print(response) 
	return response 


def query_view(request): 
	if request.method == 'POST': 
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt)
		return JsonResponse({'response': response}) 
	return render(request, 'chatbot/chatbot.html')