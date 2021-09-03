(define (problem abrir_sala_no_numeric)
    (:domain abertura_sala_no_numeric)
    (:objects 
        ct - caixa_termica
        f1 f2 f3 f4 f5 f6 f7 f8 f9 f0 - frasco
        b1 b2 b3 - bobina
        g - geladeira
    )
    (:init
        (frasco_na_geladeira f1 g)
        (frasco_na_geladeira f2 g)
        (frasco_na_geladeira f3 g)
        (frasco_na_geladeira f4 g)
        (frasco_na_geladeira f5 g)
        (frasco_na_geladeira f6 g)
        (frasco_na_geladeira f7 g)
        (frasco_na_geladeira f8 g)
        (frasco_na_geladeira f9 g)
        (frasco_na_geladeira f0 g)

        ; (= (dias_para_vencer f1) 1)
        ; (= (dias_para_vencer f2) 8)
        ; (= (dias_para_vencer f3) 15)
        ; (= (dias_para_vencer f4) 21)
        ; (= (dias_para_vencer f5) -2)
        ; (= (dias_para_vencer f6) 3)
        ; (= (dias_para_vencer f7) 8)
        ; (= (dias_para_vencer f8) 7)
        ; (= (dias_para_vencer f9) 30)
        ; (= (dias_para_vencer f0) 2)

        ; (= (frascos_dias_para_vencer g) 1)
        ; (= (numer_frascos_retirados g) 1)

        (bobina_na_geladeira b1 g)
        (bobina_na_geladeira b2 g)
        (bobina_na_geladeira b3 g)

        (geladeira_fechada g)
    )

    (:goal (and
            ; (not (frasco_estabilizando_temperatura f1))
            ; (not (frasco_na_geladeira f1 g))
            ; (bobina_na_caixa b1 ct)
        (frasco_na_caixa f1 ct)
        (frasco_na_caixa f0 ct)
        (frasco_na_caixa f6 ct)
        (frasco_na_caixa f8 ct)

        (geladeira_fechada g)
    ))

    ; (:goal (and
    ;     (= (numer_frascos_retirados) 4)
    ; ))

    ; (:metric minimize(
    ;     frascos_dias_para_vencer g
    ; ))

    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
