package com.github.danrog303.messengerstats.domain.event;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Date;

@Data
@AllArgsConstructor
public class ReactiveEvent<T> {
    private Date date;
    private ReactiveEventType type;
    private T payload;
}
