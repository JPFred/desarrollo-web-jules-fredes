package com.uchile.cc5002.avisos.controller;

import com.uchile.cc5002.avisos.dto.AvisoDTO;
import com.uchile.cc5002.avisos.entity.AvisoAdopcion;
import com.uchile.cc5002.avisos.repository.AvisoAdopcionRepository;
import com.uchile.cc5002.avisos.service.NotaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import java.util.List;
import java.util.stream.Collectors;

@Controller
public class AvisoController {
    
    @Autowired
    private AvisoAdopcionRepository avisoRepository;
    
    @Autowired
    private NotaService notaService;
    
    /**
     * Muestra el listado de avisos de adopción con sus promedios de notas
     */
    @GetMapping("/")
    public String listarAvisos(Model model) {
        List<AvisoAdopcion> avisos = avisoRepository.findAll();
        
        // Convertir a DTOs y calcular promedios
        List<AvisoDTO> avisosDTO = avisos.stream()
                .map(aviso -> {
                    AvisoDTO dto = new AvisoDTO(aviso);
                    dto.setPromedio(notaService.calcularPromedio(aviso.getId()));
                    return dto;
                })
                .collect(Collectors.toList());
        
        model.addAttribute("avisos", avisosDTO);
        return "listado-avisos";
    }
}
