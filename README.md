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
    "PLA+": 90000
  },
  "electricidad_kwh": 968,
  "consumo_kw_por_hora": 0.5,
  "precio_impresora": 1200000,
  "vida_util_horas": 7000,
  "envio_local": 6000,
  "envio_nacional": 12000,
  "precio_hora_trabajo": 6471,
  "factor_desperdicio": 100,
  "tiempo_calentamiento": 10,
  "costo_fijo": 2000
}
```

### Parámetros de Configuración:

- **materiales**: Precios por kilogramo (COP) para cada tipo de material
- **electricidad_kwh**: Precio del kilovatio-hora en COP
- **consumo_kw_por_hora**: Consumo estimado de la impresora en kW/h
- **precio_impresora**: Costo total de la impresora en COP
- **vida_util_horas**: Horas de vida útil estimadas de la impresora
- **envio_local**: Costo de envío local en COP
- **envio_nacional**: Costo de envío nacional en COP
- **precio_hora_trabajo**: Tarifa por hora de trabajo en COP
- **factor_desperdicio**: Porcentaje de desperdicio de material para cubrir posibles reimpresiones o fallos
- **tiempo_calentamiento**: Tiempo de calentamiento aproximado en minutos
- **costo_fijo**: Costo fijo por impresión en COP (gastos administrativos, etc.)

---

## Variables de Entrada

- **Material**: Selecciona el tipo de material desde la lista disponible
- **Peso de la pieza**: Peso del objeto en gramos (por defecto: 10g)
- **Tiempo de impresión**: Duración de la impresión en horas y minutos (por defecto: 1 hora)
- **Tipo de envío**: 
  - Personal (sin costo)
  - Local (costo configurable)
  - Nacional (costo configurable)
- **Margen de utilidad**: Porcentaje de margen sobre el precio final (por defecto: 20%)
- **Tiempo de post-procesado**: Tiempo de trabajo manual (por defecto: 30 minutos)

## Uso

1. Selecciona el material desde la lista.
2. Introduce el peso del objeto (en gramos).
3. Introduce el tiempo de impresión (en horas y minutos).
4. Selecciona el tipo de envío (personal, local o nacional).
5. Ajusta el margen de utilidad deseado (por defecto 20%).
6. Configura el tiempo de post-procesado (por defecto 30 minutos).
7. Visualiza el costo total y el precio final sugerido.

---

## Fórmulas de Cálculo

### 1. **Costo de Material**
```
Costo Material = Peso (kg) × Factor Desperdicio × Precio Material (COP/kg)
```
- **Factor Desperdicio**: `1 + (porcentaje_desperdicio / 100)`
- Ejemplo: 100% de desperdicio = factor 2.0 (duplica el costo)

### 2. **Costo de Electricidad**
```
Costo Electricidad = Tiempo Total × Consumo (kW/h) × Precio kWh (COP)
```
- **Tiempo Total**: Tiempo de impresión + Tiempo de calentamiento
- Incluye el tiempo de calentamiento configurado automáticamente

### 3. **Uso de la Máquina**
```
Costo Máquina = (Tiempo Total / Vida Útil) × Precio Impresora
```
- Considera la depreciación basada en el uso real de la máquina
- Incluye tiempo de calentamiento en el cálculo

### 4. **Operación de la Máquina**
```
Costo Operación = Tiempo Impresión × Tarifa Hora × 0.25
```
- **Tiempo Impresión**: Se maneja un 25% del precio que representa el tiempo parcial de supervisión durante la impresión.

### 5. **Post-Procesado**
```
Costo Post-Procesado = Tiempo Post-Procesado × Tarifa Hora
```
- **Tiempo Post-Procesado**: Tiempo completo de trabajo manual (limpieza, acabados, etc.)
- Se aplica la tarifa completa por hora de trabajo.

### 6. **Costo Fijo**
```
Costo Fijo = Valor Configurado
```
- Costo fijo por impresión independiente del tamaño o tiempo.

### 7. **Costo de Envío**
- **Personal**: $0
- **Local**: Costo configurado
- **Nacional**: Costo configurado

### 8. **Precio Final**
```
Precio Final = Costo Total / (1 - Margen Utilidad)
```
- **Costo Total**: Suma de todos los costos anteriores
- **Margen de Utilidad**: Porcentaje sobre el precio final (no sobre el costo)

### Recomendaciones de Margen de Utilidad
- **Impresiones pequeñas**: 50%
- **Impresiones medianas**: 30%
- **Impresiones grandes**: 15%

---

## Licencia

Este proyecto está licenciado bajo la MIT License.

---

## Autor

**ozkar-co**

---

## Crear Ejecutable para Linux

### Requisitos
- Python 3.7+
- pip

### Pasos para crear el ejecutable:

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar el script de build:**
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```

3. **O ejecutar PyInstaller manualmente:**
   ```bash
   pyinstaller --onefile --windowed --name FabriCalc --add-data "config.json:." main.py
   ```

### Resultado
- El ejecutable se creará en la carpeta `dist/`
- Nombre del archivo: `FabriCalc`
- Incluye automáticamente el archivo `config.json`

### Notas
- El ejecutable será específico para la arquitectura donde se compile
- Para distribuir, compila en el mismo tipo de sistema donde se usará
- El archivo resultante será independiente (no requiere Python instalado) 