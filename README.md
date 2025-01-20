# 🚀 **Urban.Routes ~ Pruebas automatizadas del proceso para pedir un Taxi**  
Conjunto de pruebas automatizadas para validar el proceso de peticion de un taxi en la plataforma.

---
## 📃 **Documentacion del proceso para pedir un taxi**
[Documentacion](https://drive.google.com/file/d/1_a8y4mFknLCA1i_QHo-ODexj1dAQpZWk/view?usp=sharing)

## 📝 **Descripción**  
Este proyecto contiene pruebas automatizadas para validar cada uno de los pasos implicados en el proceso de peticion de un taxi en la plataforma Urban.Routes.

---

## 📋 **Requisitos**  

Asegúrate de tener instaladas las siguientes herramientas:

- **Python >= 3.x**
- [Librerías necesarias](#my-custom-anchor-instalacion) (`selenium` y `pytest`)
- Archivo `main.py` para manejar solicitudes HTTP.
- Archivo `data.py` datos de prueba y direcciones URL

---

## ⚙️ **Estructura del Proyecto**  

```
📂 proyecto
       │-- main.py                       # Archivo principal con pruebas automatizadas
       │-- data.py                       # Datos de prueba y direcciones URL
       │-- requirements.txt              # Contiene la lista de dependencias para poder ejecutar correctamente el proyecto
       📂 helpers                       # Contiene codigo para el POM y calculos necesarios
              │-- pom_helpers.py         # Funciones generalizadas para interactuar con paginas y funciones de espera
              │-- util_helpers.py        # Funciones utiles para convertir unidades y extraer logs importantes de las paginas
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
   git clone https://github.com/quserforgitp/qa-project-Urban-Routes-es.git
   cd qa-project-Urban-Routes-es
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

| **Prueba**                                                      | **Descripción**                                                                                  | **Resultado Esperado**                                                                                              |
|-----------------------------------------------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `test_set_route`                                                | Verificar que las direcciones de origen y destino se establecen correctamente en la ruta.       | La dirección en el campo "Desde" debe coincidir con la dirección de origen. La dirección en el campo "Hasta" debe coincidir con la dirección de destino. |
| `test_set_tariff`                                               | Comprobar que la tarifa "Comfort" se selecciona correctamente.                                    | La tarifa seleccionada debe ser "Comfort".                                                                       |
| `test_set_phone_number`                                         | Verificar que el número de teléfono ingresado coincide con el valor mostrado en la página.       | El número de teléfono ingresado debe ser igual al número que aparece en el campo de teléfono en la página.          |
| `test_set_credit_card_data`                                     | Verificar que los datos de la tarjeta de crédito ingresados coinciden con los valores mostrados. | El número de tarjeta y el código de la tarjeta deben coincidir con los datos proporcionados.                        |
| `test_set_message_for_the_driver`                               | Comprobar que el mensaje para el conductor se establece correctamente. | El mensaje para el conductor debe ser igual al que se proporcionó en los datos de prueba.                                                          |
| `test_checkbox_blanket_and_handkerchiefs_activation`            | Verificar que el checkbox de manta y pañuelos está activado correctamente. | El checkbox de manta y pañuelos debe estar seleccionado.                                                                                    |
| `test_set_icecream_quantity`                                    | Comprobar que la cantidad de helados seleccionada se establece correctamente. | El número de helados pedidos debe ser el esperado, en este caso "2".                                                                         |
| `test_searching_taxi_modal_appears`                             | Verificar que el modal de "buscando taxi" aparece correctamente. | El modal de búsqueda de taxi debe aparecer y permanecer visible hasta que el tiempo de espera expire. |
| `test_driver_info_appears`                                      | Verificar que la información del conductor aparece correctamente en el modal después de la búsqueda.    | El nombre, la URL de la imagen y la calificación del conductor no deben estar vacíos.                             |
| `test_call_a_taxi`                                              | Verificar el proceso completo de llamar un taxi, desde la selección de la tarifa hasta la confirmación.  | El proceso debe completarse correctamente con la visualización de la información del conductor.                   |


---

## ▶️ **Ejecución de las Pruebas**  
> [!WARNING]
> Recuerda actualizar la URL de la app en el archivo `data.py` en la variable `urban_routes_url` para que las pruebas se ejecuten correctamente

![image](https://github.com/user-attachments/assets/3016c134-45d1-4d67-82e6-af2eeecaeead)


> [!NOTE]  
> ✅ Usuarios de PyCharm:
> Si quieres ejecutar las pruebas directamente en PyCharm, sigue estos pasos

![ejemplo_ejecucion_pruebas_selenium_pycharm-gif](https://github.com/user-attachments/assets/79673484-adeb-4f23-8d87-30796bfd471f)


*O si prefieres tambien las puedes ejecutar utilizando el siguiente comando:*

```bash
python -m pytest main.TestUrbanRoutes
```

---

## 📚 **Explicación del Código**  

### **Clase POM UrbanRoutesPage**
   #### **Resumen**
   - Esta clase es parte de un modelo de objetos de página (`Page Object Model`) que facilita la interacción con los elementos de la página de rutas urbanas en una aplicación. Se encarga de manejar la entrada de direcciones en los campos de origen y destino, hacer clic en los botones correspondientes, y asegurarse de que los elementos sean visibles antes de realizar cualquier acción. Utiliza tiempos de espera configurables para mejorar la estabilidad de las interacciones, asegurando que todos los elementos estén disponibles para la acción antes de proceder.


### **Resumen de Funciones Principales**  

> **`__init__(driver, search_element_timeout=5, visual_review_timeout=3)`**
- Constructor de la clase, inicializa el controlador (`driver`) y establece los tiempos de espera para recuperar elementos de la página y para inspección visual.
  
> **`set_from(from_address)`**
- Establece la dirección de origen en el formulario de la página. Recibe la dirección de origen como parámetro y la asigna al campo correspondiente en el formulario.

> **`set_to(to_address)`**
- Establece la dirección de destino en el formulario de la página. Recibe la dirección de destino como parámetro y la asigna al campo correspondiente en el formulario.

> **`__click_on_element(element_locator)`**
- Realiza un clic en el elemento indicado por su localizador (`element_locator`). Espera hasta que el elemento esté visible y luego lo hace clic. Después, espera la inspección visual.

> **`__scroll_into_element(element_locator)`**
- Desplaza la página hasta que el elemento indicado por su localizador (`element_locator`) sea visible. Luego, realiza una espera para la inspección visual.

---

### **Resumen de Funciones Auxiliares**  

> **`__set_element_text(element_locator, text)`**
- Método privado que establece el texto en un campo de texto determinado por el `element_locator`. Utiliza la espera para asegurarse de que el campo esté visible antes de enviar el texto.

> **`wait_for_visual_review()`**
- Método auxiliar que espera el tiempo configurado para la revisión visual, asegurándose de que la página esté lista para ser revisada visualmente después de una acción.

---

### **Algunos Localizadores de Elementos**  

> **`from_field_locator`**
- Localizador para el campo de "Desde" en el formulario. Usualmente se identifica por el ID `'from'`.

> **`to_field_locator`**
- Localizador para el campo de "Hasta" en el formulario. Usualmente se identifica por el ID `'to'`. 

---

### **Clase de Tests TestUrbanRoutes**
   #### **Resumen**
   - La clase `TestUrbanRoutes` implementa pruebas para verificar la funcionalidad principal de la página de rutas urbanas. Usa un enfoque sistemático para:
   - Establecer y verificar las direcciones de origen y destino.
   - Validar la selección de una tarifa específica, garantizando la interacción correcta con los elementos de la interfaz de usuario.
   - Las pruebas aprovechan un controlador configurado con capacidades avanzadas, asegurando robustez y flexibilidad en el entorno de prueba. Además, las aserciones claras y los mensajes de error detallados facilitan la depuración de problemas en caso de fallas.



#### **Resumen de Funciones Principales**  

> **`setup_class(cls)`**
- Método de configuración de clase para inicializar el controlador de Selenium antes de ejecutar las pruebas.  
- Usa opciones de Chrome para habilitar un registro de rendimiento detallado (`performance`) que facilita la captura de información adicional, como códigos de confirmación.  
- Se ejecuta una vez por clase y establece un controlador (`driver`) para ser usado por las pruebas.

> **`test_set_route(search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT)`**
- Comprueba que los campos de entrada de direcciones en la página permiten establecer correctamente una ruta.  
- Pasos principales:
  1. Maximiza la ventana del navegador.
  2. Navega a la página de rutas urbanas.
  3. Usa la clase `UrbanRoutesPage` para establecer las direcciones "Desde" y "Hasta" usando valores de prueba (`address_from` y `address_to`).
  4. Verifica que las direcciones ingresadas coincidan con los valores de prueba, lanzando un mensaje de error si no coinciden.

> **`test_set_tariff(search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT)`**
- Verifica que se puede seleccionar correctamente la tarifa "Comfort" en la página.  
- Pasos principales:
  1. Maximiza la ventana del navegador.
  2. Abre la página de rutas urbanas.
  3. Limpia el almacenamiento local para evitar configuraciones previas.
  4. Establece una ruta con valores de prueba.
  5. Simula hacer clic en "Llamar un taxi" y selecciona la tarjeta de tarifa "Comfort".
  6. Recupera la tarifa seleccionada y asegura que sea "Comfort". Muestra un mensaje de error si no coincide.

---

### **Resumen de Funciones Auxiliares y Configuración**

> **Variables de Clase**
- **`driver`**: Controlador de Selenium compartido entre las pruebas.  
- **`SEARCH_TIMEOUT`**: Tiempo de espera máximo para localizar elementos en la página (por defecto 5 segundos).  
- **`VISUAL_TIME0UT`**: Tiempo de espera adicional para revisión visual (por defecto 0 segundos).

---

## 🛠️ **Extensiones y Mejoras Futuras**

- Agregar más pruebas a métodos privados que faciliten la creación de otros métodos que interactúen con los elementos de la página.  
- Generar reportes de pruebas con herramientas como `pytest-html`.  
- **Agregar al README**:
  - Explicación sobre cómo utilizar los *timeouts* globales, aclarando que el `search_timeout` debe ser al menos 1 segundo mayor que el `visual_timeout` para evitar problemas.  
    - Ejemplo: Si asignamos 2 segundos a `search_timeout` y 2 segundos a `visual_timeout`, puede ocurrir que el proceso de búsqueda intente ejecutarse mientras el proceso visual aún está activo.  
    - Alternativa: Definir `search_timeout` como `visual_timeout + segundos`.
- Agregar manejo de excepciones para casos donde no se encuentran elementos por cualquier razón.  
- Renombrar los localizadores de elementos, métodos, etc., para alinearlos con la nomenclatura utilizada en la documentación de la aplicación.  
- Determinar si es mejor **hardcodear** en `search_timeout` la expresión `segundos + visual_timeout`.
  
## 💻🧪 QA Tester Info
### Nombre:   Helios Barrera Hernández
### Cohorte:  19
