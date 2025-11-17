package com.uchile.cc5002.avisos.service;

import com.uchile.cc5002.avisos.entity.Nota;
import com.uchile.cc5002.avisos.repository.NotaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class NotaService {
    
    @Autowired
    private NotaRepository notaRepository;
    
    /**
     * Calcula el promedio de notas para un aviso
     * @param avisoId ID del aviso
     * @return Promedio de notas o null si no hay notas
     */
    public Double calcularPromedio(Integer avisoId) {
        List<Nota> notas = notaRepository.findByAvisoId(avisoId);
        if (notas.isEmpty()) {
            return null;
        }
        return notas.stream()
                .mapToInt(Nota::getNota)
                .average()
                .orElse(0.0);
    }
    
    /**
     * Agrega una nueva nota a un aviso
     * @param avisoId ID del aviso
     * @param valorNota Valor de la nota (debe estar entre 1 y 7)
     * @return La nota guardada
     * @throws IllegalArgumentException si la nota no está entre 1 y 7
     */
    public Nota agregarNota(Integer avisoId, Integer valorNota) {
        if (valorNota < 1 || valorNota > 7) {
            throw new IllegalArgumentException("La nota debe estar entre 1 y 7");
        }
        
        Nota nota = new Nota();
        nota.setAvisoId(avisoId);
        nota.setNota(valorNota);
        
        return notaRepository.save(nota);
    }
    
    /**
     * Obtiene todas las notas de un aviso
     * @param avisoId ID del aviso
     * @return Lista de notas
     */
    public List<Nota> obtenerNotasPorAviso(Integer avisoId) {
        return notaRepository.findByAvisoId(avisoId);
    }
}
