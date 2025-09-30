Agente mínimo con framework langgraph sin memoria pero con princios de REACT (Reasoning + acting): se sigue un flujo donde el modelo evalua la pertinencia de las herramientas o funciones que conoce y luego de la ejecución o uso de las mismas (si corresponde), evalua la pertinencia de la respuesta.

# Requisitos y setup

Se debe copiar el archivo .env.example, renombrar la copia .env y agregar las siguientes variables:

-Si se va a usar un modelo via API, se necesita agregar en el archivo env el API token correspondiente. Si se va a usar modelo local via Ollama no es necesario.
-En el env también se debe agregar las variable LANGSMITH_API_KEY (se debe obtener la misma tras crear un usuario en langsmith).
Se debe crear un entorno virtual y se debe correr pip install -e . , de esa forma se instalan dependencias y librerías desde el pyproject.toml

# Deployment

Es óptimo contar con docker.

Se activa el entorno virtual, y, estando dentro de la carpeta del proyecto, se corre langgraph up. Esto lanza la interface visual del agente en local host, gracias a que docker cuenta con una imagen del UI de langsmith. 

# Funcionamiento

El script principal del agente esta en src/agent/graph.py. Este a su vez se vale del script fuente_informacion.py que maneja todos los procesos de búsqueda de información. Se puede ajustar o mejorar el SystemMessage (el prompt, esta en graph.py) dependiendo de la información que se desea que provea el agente. fuente_informacion.py actualmente está hecho a manera de ejemplo tomando de este tutorial: https://medium.com/@lachlan.chavasse/how-to-build-a-rag-agent-with-langgraph-38494a95836d

# Agregar librerías o componentes

Para agregar librerías, se deben listar las mismas en la sección dependencies del pyproject.toml. Luego se debe nuevamente correr pip install -e . 
Se debe nuevamente correr langgraph up para que impacten en el proyecto. 


