package com.example.wepapelima.repository;

import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.IntStream;

@Repository
public class ListRepository {

    private final List<ArrayList<Integer>> listStorage = new ArrayList<>();

    public List<Integer> getVersions() {
        return IntStream.rangeClosed(0, listStorage.size() - 1).boxed().toList();
    }

    public Optional<List<Integer>> getList(int id) {
        return id < listStorage.size() ? Optional.of(listStorage.get(id)) : Optional.empty();
    }

    public int insertElement(Integer newElement) {
        ArrayList<Integer> lastList = getLastList();
        lastList.add(newElement);
        listStorage.add(lastList);
        return listStorage.size() - 1;
    }

    public int removeElement(Integer oldElement) {
        ArrayList<Integer> lastList = getLastList();
        lastList.remove(oldElement);
        listStorage.add(lastList);
        return listStorage.size() - 1;
    }

    public int updateElement(Integer oldElement, Integer newElement) {
        ArrayList<Integer> lastList = getLastList();
        lastList.set(lastList.indexOf(oldElement), newElement);
        listStorage.add(lastList);
        return listStorage.size() - 1;
    }

    public boolean contains(Integer element) {
        if (listStorage.isEmpty()) {
            return false;
        }

        return listStorage.get(listStorage.size() - 1).contains(element);
    }

    private ArrayList<Integer> getLastList() {
        return listStorage.isEmpty() ? new ArrayList<>() : new ArrayList<>(listStorage.get(listStorage.size() - 1));
    }
}
