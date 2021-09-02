(define (problem desmontar_caixa)
    (:domain fechamento_sala)
    (:objects 
        ct - caixa_termica
    )
    (:init
        (ct_montada ct) 
    )

    (:goal (and
        (not (ct_montada ct))
    ))

    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
