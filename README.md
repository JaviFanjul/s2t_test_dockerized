# Speech-to-Text (S2T) - Implementaciones para Linux

Este repositorio contiene dos implementaciones del sistema de transcripción de voz a texto (S2T), diseñadas específicamente para su ejecución en entornos Linux, junto con un módulo adicional para simular micrófonos virtuales.

## 📁 Estructura del repositorio

### 1. `s2t-dockerized/`
Versión del sistema S2T preparada para ejecutarse dentro de un contenedor Docker en sistemas Linux.

- Incluye un entorno completo para ejecutar la transcripción de voz utilizando el backend de audio del sistema operativo.
- Compatible con pruebas de audio automatizadas mediante PulseAudio y dispositivos virtuales.
- Dentro del código fuente se encuentra un archivo de configuración (`config`) para ajustar todos los parámetros del programa.
- El sistema está preconfigurado para utilizar los micrófonos virtuales generados por el módulo `virtual_mics_docker`.

⚠️ **Es obligatorio haber creado los micrófonos virtuales antes de ejecutar este programa.**

---

### 2. `virtual_mics_docker/`
Módulo para la creación y gestión de micrófonos virtuales en sistemas Linux.

- Simula múltiples fuentes de audio para pruebas de transcripción en tiempo real.
- Requiere acceso al backend de audio del sistema (como PulseAudio).
- Diseñado para integrarse fácilmente con el contenedor principal del sistema S2T (`s2t-dockerized`).

---

## 📝 Notas finales

- Ambos módulos están pensados exclusivamente para **entornos Linux**, debido a su dependencia del backend de audio del sistema operativo.
- Se recomienda revisar los `README.md` individuales dentro de cada carpeta para obtener detalles técnicos, configuraciones específicas y ejemplos de uso.
- En caso de problemas con `docker-compose`, ambos contenedores pueden ejecutarse por separado utilizando los respectivos `Makefile` de cada carpeta.

---

**Autor**: Javi  
**Licencia**: MIT
