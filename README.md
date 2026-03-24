# Calculadora de Consumo Eléctrico para Centros Escolares

Herramienta web diseñada para calcular y estimar el consumo energético de sistemas de aire acondicionado en instituciones educativas, facilitando la realización de informes de auditoría energética y planes de eficiencia.

## 📋 Descripción del Proyecto

Esta aplicación permite a estudiantes, docentes y personal administrativo de centros escolares estimar el consumo eléctrico mensual y anual de sus sistemas de climatización. Es particularmente útil para:
- Elaborar informes de consumo energético requeridos en asignaturas de ciencias o tecnología
- Identificar oportunidades de ahorro energético
- Educar sobre el impacto ambiental del uso de aire acondicionado
- Proporcionar datos objetivos para toma de decisiones en gestión de instalaciones

La calculadora tiene en cuenta factores clave como:
- Potencia del equipo (en BTU o toneladas)
- Horas de uso diario y días por mes
- Eficiencia energética (SEER o EER)
- Tarifa eléctrica local
- Número de equipos similares en funcionamiento

## 🛠️ Tecnologías Utilizadas

### Frontend
- **[Astro 6](https://astro.build)** - Framework moderno para construir sitios web rápidos con enfoque en contenido
- **[Tailwind CSS 4](https://tailwindcss.com)** - Framework de CSS utility-first para diseños responsivos y personalizables
- **[Pyodide](https://pyodide.org)** - Distribución de Python para WebAssembly que ejecuta Python directamente en el navegador

### ¿Por qué esta combinación?
- **Astro** ofrece rendimiento óptimo mediante generación estática y hidratación selectiva
- **Tailwind** permite crear interfaces profesionales sin escribir CSS personalizado extensivo
- **Pyodide** Se optó por usar esta librería en lugar de TypeScript, principalmente porque era obligatorio integrar Python en la app :[

## 🚀 Comenzando

### Prerrequisitos
- [Bun](https://bun.sh) (versión 1.0 o superior)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Instalación
```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd calculadoraconsumo

# Instalar dependencias
bun install
```

### Desarrollo
```bash
# Iniciar servidor de desarrollo en http://localhost:4321
bun dev
```

### Producción
```bash
# Construir para producción
bun build

# Previsualizar la build localmente
bun preview
```

## 📖 Uso de la Aplicación

1. **Acceder a la aplicación**: Abrir `http://localhost:4321` en el navegador (en desarrollo) o desplegar la carpeta `dist/` en cualquier servidor estático
2. **Ingresar parámetros**:
   - Selecciónar tipo y cantidad de equipos de aire acondicionado
   - Especificar horas de uso diario y días de operación por mes
   - Introducir la tarifa eléctrica local (en $/kWh)
   - Opcional: ajustar valores de eficiencia SEER/EER si se conocen
3. **Visualizar resultados**:
   - Consumo mensual y anual en kWh
   - Costo estimado mensual y anual
   - Comparación con referencia de consumo típico escolar
   - Gráfica de distribución de consumo por tipo de equipo

## 🔬 Cómo Funciona Internamente

### Ejecución de Python en el Navegador
El núcleo de cálculo utiliza Pyodide para:
1. Cargar una distribución completa de Python 3.11+ en el navegador mediante WebAssembly
2. Ejecutar funciones de cálculo termoenergético sin comunicación con servidor
3. Mantener privacidad de los datos (ninguna información sale del dispositivo del usuario)
4. Permitir funcionalidad offline completa después de la carga inicial

### Fórmulas de Cálculo
El consumo se calcula usando:
```
Consumo Diario (kWh) = (Potencia en Watts × Horas de Uso) / 1000
Consumo Mensual (kWh) = Consumo Diario × Días de Uso por Mes
Costo Mensual ($) = Consumo Mensual × Tarifa Eléctrica
```

Donde la potencia en Watts se deriva de:
- BTU/h → Watts: Dividir entre 3.412
- Toneladas de refrigeración → Watts: Multiplicar por 3517
- Se ajusta según el factor de eficiencia estacional (SEER)

## 📁 Estructura del Proyecto
```
calculadoraconsumo/
├── public/           # Assets estáticos (favicon, etc.)
├── src/
│   ├── assets/       # Imágenes, iconos
│   ├── components/   # Componentes reutilizables de UI
│   │   ├── CalculatorForm.astro
│   │   ├── ResultsCard.astro
│   │   └── EfficiencyChart.astro
│   ├── layouts/      # Layouts de página
│   │   └── Layout.astro
│   └── pages/        # Rutas de la aplicación
│       └── index.astro
├── dist/             # Build de producción (generado)
├── package.json      # Dependencias y scripts
└── astro.config.mjs  # Configuración de Astro
```

## 📄 Licencia

Este proyecto es de código abierto y disponible para uso bajo la licencia MIT. Siéntete libre de adaptarlo para tus necesidades específicas.

---

*Desarrollado como herramienta educativa para promover la conciencia energética en instituciones académicas.*