package com.uchile.cc5002.avisos.controller;

import com.uchile.cc5002.avisos.entity.Nota;
import com.uchile.cc5002.avisos.service.NotaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/avisos")
public class NotaRestController {
    
    @Autowired
    private NotaService notaService;
    
    /**
     * Endpoint para agregar una nota a un aviso de forma asíncrona
     * @param avisoId ID del aviso
     * @param request Objeto con la nota a agregar
     * @return JSON con resultado de la operación y el nuevo promedio
     */
    @PostMapping("/{avisoId}/notas")
    public ResponseEntity<Map<String, Object>> agregarNota(
            @PathVariable Integer avisoId,
            @RequestBody Map<String, Integer> request) {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            Integer valorNota = request.get("nota");
            
            if (valorNota == null) {
                response.put("success", false);
                response.put("error", "El campo 'nota' es requerido");
                return ResponseEntity.badRequest().body(response);
            }
            
            // Agregar la nota
            Nota nota = notaService.agregarNota(avisoId, valorNota);
            
            // Calcular el nuevo promedio
            Double promedio = notaService.calcularPromedio(avisoId);
            
            response.put("success", true);
            response.put("nota", nota);
            response.put("promedio", promedio);
            response.put("promedioFormateado", String.format("%.1f", promedio));
            
            return ResponseEntity.ok(response);
            
        } catch (IllegalArgumentException e) {
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(response);
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", "Error al procesar la solicitud: " + e.getMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }
}
