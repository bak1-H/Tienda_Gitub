# Manual de Usuario

Este manual te guía para usar la aplicación de tienda construida con Flask: iniciar sesión, crear órdenes, emitir facturas y registrar despachos.

## 1. Requisitos
- Navegador web (Chrome/Edge/Firefox).
- Servicio en ejecución local (`http://localhost:5000`) o desplegado en Render.
- Usuario con credenciales. En desarrollo puedes crear `admin/admin` visitando `/auth/seed`.

## 2. Acceso y autenticación
1. Abre la URL del servicio.
2. Ve a `Auth → Login` o visita `/auth/login`.
3. Ingresa `usuario` y `contraseña`.
4. Si son correctos, verás el menú principal.

Opcional: Registro
- Ve a `Auth → Registro` (si está habilitado) y crea un usuario.

## 3. Menú principal
- Acceso a creación de Orden de Compra (OC).
- Listado de órdenes existentes (con acciones para facturar y despachar).
- Botón para cerrar sesión.

## 4. Crear una Orden de Compra (OC)
1. Desde el menú, elige "Crear orden".
2. Completa datos del cliente:
   - Número de orden (debe ser único; si se repite, el sistema te avisará).
   - Nombre, dirección, teléfono, comuna y región.
3. Agrega productos (múltiples líneas):
   - Nombre del producto.
   - Precio (en pesos).
   - Cantidad.
   - Las líneas vacías se omiten.
4. Guarda la orden. Si todo es válido, la OC se lista en el menú.

Consejos:
- Evita duplicar el número de orden.
- Usa precios y cantidades numéricas válidas.

## 5. Emitir una factura
1. En el listado de órdenes, elige "Facturar" sobre la OC deseada.
2. El sistema calcula automáticamente:
   - Neto: suma de (precio × cantidad) por ítem.
   - IVA (19%): neto × 0.19.
   - Total con impuesto: neto + IVA.
3. Se crea la factura y la orden pasa a estado "facturada".
4. Puedes ver el detalle de la factura.

Restricciones:
- Una sola factura por orden.

## 6. Registrar despacho
1. En el detalle de la factura, elige "Despachar".
2. Ingresa una nota de despacho (opcional).
3. Se crea el despacho y la orden pasa a estado "despachada".

## 7. Cerrar sesión
- Usa el botón "Cerrar sesión" en la barra superior o ve a `/auth/logout`.

## 8. Estados y mensajes
- Estados de la OC: "creada" → "facturada" → "despachada".
- Mensajes comunes:
  - "Número de orden ya existe": cambia el número de orden y vuelve a intentar.
  - Errores de validación: revisa precios/cantidades y campos obligatorios.

## 9. Solución de problemas
- No puedes iniciar sesión:
  - Verifica usuario/contraseña; en desarrollo crea `admin/admin` en `/auth/seed`.
- No se crea la orden:
  - Revisa que el número de orden no esté repetido.
  - Asegúrate de llenar datos del cliente y al menos un producto válido.
- Error al facturar:
  - La orden ya podría estar facturada.
  - Verifica que existan ítems con cantidades y precios válidos.
- Error al despachar:
  - Asegúrate de que la orden esté facturada antes de despachar.

## 10. Glosario
- **OC**: Orden de Compra.
- **IVA**: Impuesto al Valor Agregado; por defecto 19%.
- **Factura**: Documento que resume neto, IVA y total de la OC.
- **Despacho**: Registro del envío asociado a la factura.

## 11. Contacto
- Si despliegas en Render, revisa los logs del servicio ante errores.
- Para soporte técnico, consulta el `README` del repositorio o abre un issue.
