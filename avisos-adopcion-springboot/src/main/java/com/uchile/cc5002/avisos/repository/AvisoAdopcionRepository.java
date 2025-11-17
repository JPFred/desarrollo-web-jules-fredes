package com.uchile.cc5002.avisos.repository;

import com.uchile.cc5002.avisos.entity.AvisoAdopcion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AvisoAdopcionRepository extends JpaRepository<AvisoAdopcion, Integer> {
}
