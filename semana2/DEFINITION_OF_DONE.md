# Definition of Done (DoD) - Semana 2

Para que una Historia de Usuario (US) se considere "Terminada", debe cumplir estrictamente con los siguientes criterios:

- [ ] **Tests Automatizados:** Los criterios de aceptación (escenarios Gherkin) están implementados como pruebas en `pytest`.
- [ ] **Cobertura de Código:** La cobertura de pruebas es mayor o igual al 80%.
- [ ] **Calidad de Código (Linters):** El código pasa la validación de `ruff` sin advertencias ni errores.
- [ ] **Tipado Estricto:** El análisis estático con `mypy` está limpio y cumple con `disallow_untyped_defs`.
- [ ] **Auto-Revisión (PR):** Se realizó una lectura del diff línea por línea en un Pull Request antes del merge.
- [ ] **Documentación:** La bitácora (AI_LOG.md) y los diagramas están actualizados.