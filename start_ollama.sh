docker run -d \
  -p 11434:11434 \
  -v /home/quinn/.ollama:/root/.ollama \
  --name ollama \
  ollama/ollama
