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

    public static <T> ReactiveEvent<T> eventInfoOf(T payload) {
        return new ReactiveEvent<>(new Date(), ReactiveEventType.EVENT_INFO, payload);
    }

    public static <T> ReactiveEvent<T> dataPortionOf(T payload) {
        return new ReactiveEvent<>(new Date(), ReactiveEventType.DATA_PORTION, payload);
    }
}
