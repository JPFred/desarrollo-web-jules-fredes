package com.uchile.cc5002.avisos.dto;

import com.uchile.cc5002.avisos.entity.AvisoAdopcion;
import java.time.format.DateTimeFormatter;

public class AvisoDTO {
    private Integer id;
    private String fechaPublicacion;
    private String sector;
    private String cantidadTipoEdad;
    private String comuna;
    private Double promedio;
    
    public AvisoDTO(AvisoAdopcion aviso) {
        this.id = aviso.getId();
        
        // Formatear fecha
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        this.fechaPublicacion = aviso.getFechaIngreso().format(formatter);
        
        this.sector = aviso.getSector();
        
        // Construir descripción "cantidad tipo edad"
        String tipoPlural = aviso.getTipo();
        if (aviso.getCantidad() > 1) {
            tipoPlural = aviso.getTipo().equals("gato") ? "gatos" : "perros";
        }
        
        String unidad = aviso.getUnidadMedida().equals("a") ? "años" : "meses";
        if (aviso.getEdad() == 1) {
            unidad = aviso.getUnidadMedida().equals("a") ? "año" : "mes";
        }
        
        this.cantidadTipoEdad = String.format("%d %s %d %s", 
            aviso.getCantidad(), tipoPlural, aviso.getEdad(), unidad);
        
        this.comuna = aviso.getComuna().getNombre();
    }
    
    public String getPromedioFormatted() {
        if (promedio == null) {
            return "-";
        }
        return String.format("%.1f", promedio);
    }
    
    // Getters y Setters
    public Integer getId() {
        return id;
    }
    
    public void setId(Integer id) {
        this.id = id;
    }
    
    public String getFechaPublicacion() {
        return fechaPublicacion;
    }
    
    public void setFechaPublicacion(String fechaPublicacion) {
        this.fechaPublicacion = fechaPublicacion;
    }
    
    public String getSector() {
        return sector;
    }
    
    public void setSector(String sector) {
        this.sector = sector;
    }
    
    public String getCantidadTipoEdad() {
        return cantidadTipoEdad;
    }
    
    public void setCantidadTipoEdad(String cantidadTipoEdad) {
        this.cantidadTipoEdad = cantidadTipoEdad;
    }
    
    public String getComuna() {
        return comuna;
    }
    
    public void setComuna(String comuna) {
        this.comuna = comuna;
    }
    
    public Double getPromedio() {
        return promedio;
    }
    
    public void setPromedio(Double promedio) {
        this.promedio = promedio;
    }
}
