package com.uchile.cc5002.avisos.repository;

import com.uchile.cc5002.avisos.entity.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
    List<Nota> findByAvisoId(Integer avisoId);
}
