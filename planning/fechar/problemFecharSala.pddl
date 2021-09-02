(define (problem fechar_sala)
    (:domain fechamento_sala)
    (:objects 
        ct - caixa_termica
        f1 f2 f3 f4 f5 - frasco
        b1 b2 b3 - bobina
        g - geladeira

    )
    (:init
        (ct_montada ct)
        (frasco_vencido f1)
        (frasco_vencido f3)
        (frasco_vencido f5)
        (frasco_na_caixa f1 ct)
        (frasco_na_caixa f2 ct)
        (frasco_na_caixa f3 ct)
        (frasco_na_caixa f4 ct)
        (frasco_na_caixa f5 ct)

        (bobina_na_caixa b1 ct)
        (bobina_na_caixa b2 ct)
        (bobina_na_caixa b3 ct)

        (geladeira_ligada g)
        (geladeira_fechada g)
    )

    (:goal (and
        (bobina_guardada b1)
        (bobina_guardada b2)
        (bobina_guardada b3)

        (ct_sem_bobinas  ct)
        (ct_sem_frascos  ct)

        (geladeira_ligada g)
        (geladeira_fechada g)
    ))

    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
