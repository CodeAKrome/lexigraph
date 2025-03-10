qwen72bsolar:
	./test_llm.sh ollama 'qwen2.5:72b' solar.txt "Where is best for seeing the Aurora?"
qwen72bsolarm:
	./test_llm.sh ollama 'qwen2.5:72b' solar_m.txt "Where is best for seeing the Aurora?"
llama70bsolar:
	./test_llm.sh ollama 'llama3.1:70b' solar.txt "Where is best for seeing the Aurora?"
llama70bsolarm:
	./test_llm.sh ollama 'llama3.1:70b' solar_m.txt "Where is best for seeing the Aurora?"
llama70brag:
	./test_llm.sh ollama 'llama3.1:70b' rag.txt "What are the chances of peace in Ukraine?"
llama70bragm:
	./test_llm.sh ollama 'llama3.1:70b' rag_m.txt "What are the chances of peace in Ukraine?"
samba405bsolar:
	./test_llm.sh sambanova 'Meta-Llama-3.1-405B-Instruct' solar.txt "Where is best for seeing the Aurora and why?"
samba405bsolarm:
	./test_llm.sh sambanova 'Meta-Llama-3.1-405B-Instruct' solar_m.txt "Where is best for seeing the Aurora and why?"
samba405brag:
	./test_llm.sh sambanova 'Meta-Llama-3.1-405B-Instruct' rag.txt "What are the chances of peace in Ukraine?"
samba405bragm:
	./test_llm.sh sambanova 'Meta-Llama-3.1-405B-Instruct' rag_m.txt "What are the chances of peace in Ukraine?"
gemini-flashrag:
	./test_llm.sh gemini gemini-1.5-flash rag.txt "What are the chances of peace in Ukraine?"
gemini-flashragm:
	./test_llm.sh gemini gemini-1.5-flash rag_m.txt "What are the chances of peace in Ukraine?"
gemini-prorag:
	./test_llm.sh gemini gemini-1.5-pro rag.txt "What are the chances of peace in Ukraine?"
gemini-proragm:
	./test_llm.sh gemini gemini-1.5-pro rag_m.txt "What are the chances of peace in Ukraine?"
cmdrrag:
	./test_llm.sh ollama 'command-r-plus:latest' rag.txt "What are the chances of peace in Ukraine?"
cmdrragm:
	./test_llm.sh ollama 'command-r-plus:latest' rag_m.txt "What are the chances of peace in Ukraine?"
llavarag:
	./test_llm.sh ollama 'llava:34b' rag.txt "What are the chances of peace in Ukraine?"
llavaragm:
	./test_llm.sh ollama 'llava:34b' rag_m.txt "What are the chances of peace in Ukraine?"
