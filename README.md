# App Server de MeLi

[![Build Status](https://travis-ci.org/estanislaoledesma/app-server-meli.svg?branch=master)](https://travis-ci.org/estanislaoledesma/app-server-meli) [![codecov.io](https://codecov.io/gh/estanislaoledesma/app-server-meli/badge.svg)](https://codecov.io/gh/estanislaoledesma/app-server-meli?branch=master)

## Definición

Se trata de un sistema que permite la gestión de compra-venta de porductos por usuarios registrados. Permite la calificación de usuarios en base a las compras realizadas, la gestión de preguntas y respuestas de productos publicados y la estimación de costos de envíos de las compras.

## Desarrollo

Para poder desarrollar, se debe clonar el proyecto y desde la carpeta principal, por terminal, ejecutar el siguiente comando:

```bash
gunicorn -w <No_Of_Workers> src.server:app
```

## Link

[App Server Meli](http://app-server-meli.herokuapp.com/)

## Documentos

[Manual de Usuario](https://docs.google.com/document/d/10grr-TEky_t54K10r6Id9k1ZLeeAz-yt8_viIT_9qqU/edit?usp=sharing)

[Definiciones de Diseño y Arquitectura](https://docs.google.com/document/d/1gFpoZqph1Wu6w0HQnk_allr0uSNBMnI-DyFDHyPwzHw/edit?usp=sharing)
