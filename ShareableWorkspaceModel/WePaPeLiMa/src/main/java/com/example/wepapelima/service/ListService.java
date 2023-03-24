package com.example.wepapelima.service;

import com.example.wepapelima.exception.DeletingElementNotExistsException;
import com.example.wepapelima.exception.ListNotExistsException;
import com.example.wepapelima.repository.ListRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ListService {

    private final ListRepository listRepository;

    public ListService(ListRepository listRepository) {
        this.listRepository = listRepository;
    }

    public List<Integer> getVersions() {
        return listRepository.getVersions();
    }

    public List<Integer> getList(int id) {
        Optional<List<Integer>> optionalList = listRepository.getList(id);
        if (optionalList.isEmpty()) {
            throw new ListNotExistsException();
        }

        return optionalList.get();
    }

    public int insertElement(Integer newElement) {
        return listRepository.insertElement(newElement);
    }

    public int removeElement(Integer oldElement) {
        if (!listRepository.contains(oldElement)) {
            throw new DeletingElementNotExistsException();
        }

        return listRepository.removeElement(oldElement);
    }

    public int updateElement(Integer oldElement, Integer newElement) {
        if (!listRepository.contains(oldElement)) {
            throw new DeletingElementNotExistsException();
        }

        return listRepository.updateElement(oldElement, newElement);
    }
}
