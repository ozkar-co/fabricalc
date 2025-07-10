# FabriCalc

**FabriCalc** es una herramienta de código abierto para calcular el costo real de una impresión 3D, considerando materiales, tiempo, electricidad, depreciación de máquina, envío y ganancia.

Diseñada para makers, desarrolladores y emprendedores que desean estimar precios de forma técnica y ajustada a su realidad.

---

## Características

- Cálculo detallado de costos:
  - Material (por peso y tipo)
  - Tiempo de impresión
  - Electricidad (según tarifa local)
  - Depreciación de la impresora
  - Costos de envío
  - Margen de ganancia configurable
- Interfaz gráfica (Python)
- Configuración editable desde archivo externo (`config.json`)
- Pensado para uso personal o en talleres

---

## Configuración

Edita el archivo `config.json` para ajustar tus valores:

```json
{
  "materiales": {
    "PLA Wood": 150000,
    "PETG": 120000,
    "PLA+": 110000
  },
  "electricidad_kwh": 968,
  "consumo_kw_por_hora": 0.5,
  "precio_impresora": 1200000,
  "vida_util_horas": 7000,
  "envio_local": 6000,
  "envio_nacional": 12000,
  "precio_hora_trabajo": 12500
}
```

- Los precios de material son por kilogramo (COP).
- El consumo de energía es estimado (kW por hora).
- Los valores de envío son referenciales y puedes cambiarlos.

---

## Variables de Entrada

- **Material**: Selecciona el tipo de material desde la lista disponible
- **Peso de la pieza**: Peso del objeto en gramos
- **Tiempo de impresión**: Duración de la impresión en horas
- **Tipo de envío**: 
  - Personal (sin costo)
  - Local (costo configurable)
  - Nacional (costo configurable)
- **Porcentaje de ganancia**: Por defecto 40%
- **Tiempo de postprocesado**: Por defecto 20 minutos

## Uso

1. Selecciona el material desde la lista.
2. Introduce el peso del objeto (en gramos).
3. Introduce el tiempo de impresión (en horas).
4. Selecciona el tipo de envío (personal, local o nacional).
5. Ajusta el porcentaje de ganancia deseado (por defecto 40%).
6. Configura el tiempo de postprocesado (por defecto 20 minutos).
7. Visualiza el costo total y el precio final sugerido.

---

## Licencia

Este proyecto está licenciado bajo la MIT License.

---

## Autor

**ozkar-co** 