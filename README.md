# 🚀 **Urban.Routes ~ Pruebas automatizadas del proceso para pedir un Taxi**  
Conjunto de pruebas automatizadas para validar el proceso de peticion de un taxi en la plataforma.

---
## **Documentacion del proceso para pedir un taxi**
[Documentacion](https://drive.google.com/file/d/1_a8y4mFknLCA1i_QHo-ODexj1dAQpZWk/view?usp=sharing)

## 📝 **Descripción**  
Este proyecto contiene pruebas automatizadas para validar cada uno de los pasos implicados en el proceso de peticion de un taxi en la plataforma Urban.Routes.

---

## 📋 **Requisitos**  

Asegúrate de tener instaladas las siguientes herramientas:

- **Python >= 3.x**
- [Librerías necesarias](#) (`selenium` y `pytest`)
- Archivo `main.py` para manejar solicitudes HTTP.
- Archivo `data.py` que contiene un diccionario con la estructura base del cuerpo de la solicitud y headers para las requests.

---

## ⚙️ **Estructura del Proyecto**  

```
📂 proyecto
│-- main.py                        # Archivo principal con pruebas automatizadas
│-- data.py                        # Datos de prueba y direcciones URL
│-- requirements.txt               # Contiene la lista de dependencias para poder ejecutar correctamente el proyecto
```

---

## 🔧 **Instalación y Configuración**  

**1. Clona el repositorio:**

> [!NOTE]  
> ✅ Usuarios de PyCharm:
Si quieres clonar este repositorio directamente desde PyCharm, te puede interesar visitar este enlace:
[Guía oficial de PyCharm para clonar repositorios de GitHub](https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html#clone-from-GitHub)

*O bien, puedes utilizar directamente la linea de comandos*
   ```bash
   git clone [https://github.com/quserforgitp/<nombre-del-repositorio-aqui>.git]
   cd <nombre-del-repositorio-aqui>
   ```
   
**2. Instala las dependencias requeridas:**
<a name="my-custom-anchor-instalacion"></a>
> [!NOTE]  
> ✅ Usuarios de PyCharm:
Si quieres instalar las dependencias desde `requirements.txt` directamente en PyCharm, te puede interesar visitar este enlace:
[Guía oficial de PyCharm para gestionar dependencias de un `requirements.txt`](https://www.jetbrains.com/help/pycharm/managing-dependencies.html#apply_dependencies)

*O bien, puedes utilizar directamente la linea de comandos*
 ```bash
 pip install -r requirements.txt
 ```
---

## 🚦 **Casos de Prueba**  

| **Prueba**                                                               | **Descripción**               | **Resultado Esperado**           |
|--------------------------------------------------------------------------|-------------------------------|---------------------------------|
| `test_1_create_kit_for_user_1_letter_in_name_get_success_response` | El nombre tiene 1 caracter. | Código de respuesta: 201 El campo "name" del cuerpo de la respuesta coincide con el campo "name" del cuerpo de la solicitud         |



---

## ▶️ **Ejecución de las Pruebas**  
> [!WARNING]
> Recuerda actualizar la URL de la app en el archivo `data.py` en la variable `urban_routes_url` para que las pruebas se ejecuten correctamente

![image](https://github.com/user-attachments/assets/4bab705c-b81f-402a-a5f9-077082fcbd80)


> [!NOTE]  
> ✅ Usuarios de PyCharm:
> Si quieres ejecutar las pruebas directamente en PyCharm, sigue estos pasos

![Ejecutar pruebas desde PyCharm](https://github.com/user-attachments/assets/88215733-faa3-4192-8ad3-21b7600a85ee)


*O si prefieres tambien las puedes ejecutar utilizando el siguiente comando:*

```bash
python -m pytest main.TestUrbanRoutes
```

---

## 📚 **Explicación del Código**  

### **Funciones Principales**  
   > **`positive_assert(kit_name)`**

   - Verifica que la creación de un kit con el nombre proporcionado en `kit_name` sea exitosa. Valida que el código de estado sea 201 y que el campo `"name"` en la respuesta coincida con el nombre enviado.

   
### **Funciones Auxiliares**  

   > **`get_create_user_body()`**

   - Devuelve una copia del cuerpo de solicitud necesario para la creación de un usuario.

   
---

## 🛠️ **Extensiones y Mejoras Futuras**
- Agregar más pruebas metodos privados que faciliten la creacion de otros metodos que interactuen con los elementos de la pagina.
- Generar reportes de pruebas con herramientas como pytest-html.

---
