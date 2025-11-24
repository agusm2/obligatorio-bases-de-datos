# Informe 

Trabajo realizado por Mateo Di Fortuna y Agustin Maldonado para la materia Bases de Datos.

### Decisiones de implementación
- Arquitectura general
  - Separamos el backend del frontend para desacoplar la lógica del programa, y cada uno de los participantes se enfocó más en una de las partes de las arquitecturas, manteniéndonos al tanto de las implementaciones realizadas.
- Tecnologías utilizadas
  - Flask + Python: utilizadas en el back-end debido a las consideraciones realizadas por los docentes para la elaboración del proyecto; la implementación de Flask se justifica debido a que consideramos que la elaboración de la API requería ser sencilla y fácil de comprender.
  - MySQL: utilizado debido a las consideraciones solicitadas por los docentes.
  - React + Vite: utilizadas para el front-end por motivos similares a las tecnologías utilizadas en el backend; queríamos algo sencillo de implementar y conocíamos estas tecnologías de otras asignaturas como Desarrollo Web & Mobile.
  - React Bootstrap: framework utilizado a nivel de front-end para estilizar nuestra aplicación; nos decantamos por este framework ya que nuevamente era una tecnología de implementación sencilla.
- Organización del back-end
  - Separación en rutas para diferenciar claramente los endpoints, también utilizamos Postman para tener un acceso más sencillo a los mismos.
- Organización del front-end.
  - Componentes específicos para cada página según lo solicitado en la letra.
  - Uso de rutas protegias (ProtectedRoute) para redirigir al usuario según su rol (admin o usuario).
  - Guardamos al usuario en el almacenamiento del navegador para poder acceder a él y que no se pierda cuando se actualiza el mismo, así podemos ver sus atributos y navegar en base a su rol a través de las diferentes páginas definidas.

### Mejoras implementadas o consideradas en el modelo de datos
- Se considera modificar la tabla Login, añadiendo las categorías
de admin y user, para tener a personas que puedan acceder a datos sensibles,
y otras que solamente puedan acceder a esos datos.
- Se agregan restricciones a nivel de tablas agregando campos NOT NULL evitando asi tener campos vacíos.
- Se agrega el atributo AUTO_INCREMENT a campos de id_facultad, id_turno, id_alumno_programa e id_reserva; para no tener que insertar manualmente este dato.
- Agregamos propiedades default para que por defecto se establezcan datos con cierto valor para evitar modificarlos manualmente.
- Cuando se crea un participante también se crea en la tabla login para que este pueda crear reservas.
- Usamos utf8 para permitir el uso de caracteres especiales en español (ñ, tildes, etc.)
- Creamos usario llamado 'obligatorio' y le otorgamos permisos para que pueda operar sobre la tabla; de este modo se permite la conexión desde cualquier IP y poder así conectarse con Flask.

### Bitácora
1. Creación de repo y tablas.
2. Diseño de consultas seguridas por los integrantes.
3. Modificación del orden de creación de tablas para poder asignar correctamente las FKs.
4. Se modifica el login para tener diferentes tipos de usuarios como interacciones con el sistema de gestión.
5. Elección de tecnologías para front-end y back-end.
6. Diseño general de back-end (rutas, modelos y servicios) y front-end (componentes, páginas y contextos).
7. Modificamos creación de participantes para que también se creen en la tabla de login.
8. Actualizamos cómo se muestran los turnos al crear una reserva en base a su disponibilidad.
9. Algunas consultas diseñadas por nosotros, consideramos que son originales y otorgan información valiosa al usuario; sin embargo, debido a como desarrollamos nuestra aplicación, no es posible representar esos resultados para dichas consultas.

### Bibliografía
- Base de datos
  - MySQL. (s.f.). MySQL. Oracle Corporation. https://www.mysql.com/ 
- Back-end
  - Python Software Foundation. (s.f.). Python. https://www.python.org/
  - Pallets Projects. (s.f.). Flask documentation. https://flask.palletsprojects.com/en/stable/
- Front-end
  - Meta Platforms, Inc. (s.f.). React documentation. https://es.react.dev/
  - React Bootstrap Contributors. (s.f.). React-Bootstrap documentation. https://react-bootstrap.netlify.app/
- Iconos visuales
  -   Fonticons, Inc. (s.f.). Font Awesome. https://fontawesome.com/
