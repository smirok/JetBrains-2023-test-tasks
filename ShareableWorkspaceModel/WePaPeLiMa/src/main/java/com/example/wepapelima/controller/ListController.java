package com.example.wepapelima.controller;

import com.example.wepapelima.model.GetVersionsResponse;
import com.example.wepapelima.model.InsertElementRequest;
import com.example.wepapelima.model.ListVersionResponse;
import com.example.wepapelima.model.RemoveElementRequest;
import com.example.wepapelima.model.UpdateElementRequest;
import com.example.wepapelima.service.ListService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ListController {

    private final ListService listService;

    public ListController(ListService listService) {
        this.listService = listService;
    }

    @GetMapping(path = "/lists", produces = "application/json")
    public GetVersionsResponse getVersions() {
        return new GetVersionsResponse(listService.getVersions());
    }

    @GetMapping(path = "/list/{id}")
    public List<Integer> getList(@PathVariable Integer id) {
        return listService.getList(id);
    }

    @PostMapping(path = "/list", consumes = "application/json", produces = "application/json")
    public ListVersionResponse insertElement(@RequestBody @Valid InsertElementRequest insertElementRequest) {
        return new ListVersionResponse(listService.insertElement(insertElementRequest.newElement()));
    }

    @DeleteMapping(path = "/list", consumes = "application/json", produces = "application/json")
    public ListVersionResponse removeElement(@RequestBody @Valid RemoveElementRequest removeElementRequest) {
        return new ListVersionResponse(listService.removeElement(removeElementRequest.oldElement()));
    }

    @PutMapping(path = "/list", consumes = "application/json", produces = "application/json")
    public ListVersionResponse updateElement(@RequestBody @Valid UpdateElementRequest updateElementRequest) {
        return new ListVersionResponse(
                listService.updateElement(
                        updateElementRequest.oldElement(),
                        updateElementRequest.newElement()
                )
        );
    }
}
