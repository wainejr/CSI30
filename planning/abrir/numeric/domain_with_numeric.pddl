(define (domain abertura_sala_numeric)

    ;remove requirements that are not needed
    (:requirements :strips :typing :conditional-effects :negative-preconditions :numeric-fluents)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        caixa_termica frasco bobina geladeira
    )

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates ;todo: define predicates here
        (ct_separada  ?c - caixa_termica) ;; caixa termica esta montada

        (frasco_na_caixa ?f - frasco ?ct - caixa_termica) ;; frasco já foi retirado da caixa (não foi processado)
        (frasco_estabilizando_temperatura ?f - frasco) ;; frasco esperando temperatura estabilizar
        (frasco_na_geladeira ?f - frasco ?g - geladeira) ;; frasco guardado na geladeira

        (bobina_na_caixa ?b - bobina ?ct - caixa_termica) ;; bobina está na caixa
        (bobina_esquentando ?b - bobina) ;; bobina esperando temperatura estabilizar
        (bobina_na_geladeira ?b - bobina ?g - geladeira) ;; bobina está lavada

        (geladeira_fechada ?g - geladeira) ;; geladeira está fechada
    )

    (:functions
        (dias_para_vencer ?f - frasco)
        (frascos_dias_para_vencer ?g - geladeira)
        (numer_frascos_retirados ?g - geladeira)
    )

    ;define actions here
    (:action separar_caixa_termica
        :parameters (?ct - caixa_termica)
        :precondition (and 
            (not (ct_separada ?ct))
        )
        :effect (and 
            (ct_separada ?ct)
        )
    )

    (:action retirar_frasco_geladeira_fechar_geladeira
        :parameters (?f - frasco ?g - geladeira)
        :precondition (and 
            (frasco_na_geladeira ?f ?g)
            (not(geladeira_fechada ?g))
            (>= (dias_para_vencer ?f) 0)
        )
        :effect (and 
            (not (frasco_na_geladeira ?f ?g))
            (geladeira_fechada ?g)
            (frasco_estabilizando_temperatura ?f)
            (increase (frascos_dias_para_vencer ?g) (dias_para_vencer ?f))
            (increase (numer_frascos_retirados ?g) 1)
        )
    )

    (:action retirar_bobina_geladeira_fechar_geladeira
        :parameters (?b - bobina ?g - geladeira)
        :precondition (and 
            (bobina_na_geladeira ?b ?g)
            (not(geladeira_fechada ?g))
        )
        :effect (and 
            (not (bobina_na_geladeira ?b ?g))
            (geladeira_fechada ?g)
            (bobina_esquentando ?b)
        )
    )

    (:action esperar_temperatura_vacinas_estabilizar
        :parameters ()
        :precondition (and 
            (forall (?f - frasco) 
                (frasco_estabilizando_temperatura))
        )
        :effect (and
            (forall (?f - frasco) 
                (not (frasco_estabilizando_temperatura)))
        )
    )

    (:action esperar_bobinas_esquentarem
        :parameters ()
        :precondition (and 
            (forall (?b - bobina) 
                (bobina_esquentando))
        )
        :effect (and
            (forall (?b - bobina) 
                (not (bobina_esquentando)))
        )
    )

    (:action colocar_frasco_na_caixa
        :parameters (?f - frasco ?ct - caixa_termica)
        :precondition (and 
            (ct_separada ?ct)
            (not (frasco_estabilizando_temperatura ?f))
            (forall (?b - bobina) 
                (bobina_na_caixa ?b ?ct))
            (not (frasco_na_caixa ?f ?ct))
        )
        :effect (and 
            (frasco_na_caixa ?f ?ct)
        )
    )

    (:action colocar_bobina_na_caixa
        :parameters (?b - bobina ?ct - caixa_termica)
        :precondition (and 
            (ct_separada ?ct)
            (not (bobina_esquentando ?b))
            (forall (?b - bobina) 
                (bobina_na_caixa ?b ?ct))
            (not (bobina_na_caixa ?b ?ct))
        )
        :effect (and 
            (bobina_na_caixa ?b ?ct)
        )
    )

    (:action fechar_geladeira
        :parameters (?g - geladeira)
        :precondition (and 
            (not (geladeira_fechada ?g))
        )
        :effect (and (geladeira_fechada ?g))
    )

    (:action abrir_geladeira
        :parameters (?g - geladeira)
        :precondition (and 
            (geladeira_fechada ?g)
        )
        :effect (and (not (geladeira_fechada ?g)))
    )
)
