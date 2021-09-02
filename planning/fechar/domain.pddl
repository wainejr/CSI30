(define (domain fechamento_sala)

    ;remove requirements that are not needed
    (:requirements :strips :typing :conditional-effects :negative-preconditions)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        caixa_termica frasco bobina geladeira
    )

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates ;todo: define predicates here
        (ct_montada  ?c - caixa_termica) ;; caixa termica esta montada
        (ct_sem_frascos ?c - caixa_termica) ;; caixa termica não tem frascos
        (ct_sem_bobinas  ?c - caixa_termica) ;; caixa termica não tem bobinas

        (frasco_vencido  ?f - frasco) ;; frasco está vencido
        (frasco_na_caixa ?f - frasco ?ct - caixa_termica) ;; frasco já foi retirado da caixa (não foi processado)
        (frasco_processado ?f - frasco) ;; frasco já foi processado (guardado ou descartado)

        (bobina_na_caixa ?b - bobina ?ct - caixa_termica) ;; bobina está na caixa
        (bobina_lavada ?b - bobina) ;; bobina está lavada
        (bobina_guardada ?b - bobina) ;; bobina está lavada

        (geladeira_ligada ?e - geladeira) ;; geladeira está guardado ou não

        (geladeira_fechada ?g - geladeira) ;; geladeira está fechada
    )

    ;define actions here
    (:action desmontar_caixa_termica
        :parameters (?c - caixa_termica)

        :precondition (and 
            (ct_montada ?c) ;; Caixa está montada
        )

        :effect (and 
            (not (ct_montada ?c))
        )
    )

    (:action esvaziar_frascos_da_caixa
        :parameters (?ct - caixa_termica)
        :precondition (and
            ;; não há frasco na caixa
            (forall (?f - frasco) 
                (not (frasco_na_caixa ?f ?ct)))
            (not (ct_sem_frascos ?ct))
        )

        :effect (and 
            (ct_sem_frascos ?ct)
        )
    )

    (:action guardar_frasco_fechar_geladeira
        :parameters (?f - frasco ?ct - caixa_termica ?g - geladeira)
        :precondition (and 
            (not (ct_montada ?ct))
            (frasco_na_caixa ?f ?ct)
            (not (frasco_vencido ?f))
            (not (geladeira_fechada ?g))
            (geladeira_ligada ?g)
        )
        :effect (and 
            (not (frasco_na_caixa ?f ?ct))
            (frasco_processado ?f)
            (geladeira_fechada ?g)
        )
    )

    (:action descartar_frasco
        :parameters (?f - frasco ?ct - caixa_termica)
        :precondition (and 
            (not (ct_montada ?ct))
            (frasco_na_caixa ?f ?ct)
            (frasco_vencido ?f)
        )
        :effect (and 
            (not (frasco_na_caixa ?f ?ct))
        )
    )

    (:action retirar_bobina
        :parameters (?b - bobina ?ct - caixa_termica)
        :precondition (and 
            (ct_sem_frascos ?ct)
            (bobina_na_caixa ?b ?ct)
        )
        :effect (and
            (not (bobina_na_caixa ?b ?ct))
        )
    )

    (:action esvaziar_bobinas_da_caixa
        :parameters (?ct - caixa_termica)
        :precondition (and
            ;; não há bobinas na caixa
            (forall (?b - bobina) 
                (not (bobina_na_caixa ?b ?ct)))
            (not (ct_sem_bobinas ?ct))
        )

        :effect (and 
            (ct_sem_bobinas ?ct)
        )
    )

    (:action lavar_bobina
        :parameters (?b - bobina)
        :precondition (and 
            ;; bobina não está em nenhuma caixa
            (not (exists (?ct - caixa_termica)
                (bobina_na_caixa ?b ?ct)))
            (not (bobina_lavada ?b))
        )
        :effect (and
            (bobina_lavada ?b)
        )
    )

    (:action guardar_bobina_fechar_geladeira
        :parameters (?b - bobina ?g - geladeira)
        :precondition (and 
            (bobina_lavada ?b)
            (not (bobina_guardada ?b))
            (not (geladeira_fechada ?g))
            (geladeira_ligada ?g)
        )
        :effect (and
            (bobina_guardada ?b)
            (geladeira_fechada ?g)
        )
    )

    (:action ligar_geladeira
        :parameters (?g - geladeira)
        :precondition (and 
            (not (geladeira_ligada ?g))
        )
        :effect (and 
            (geladeira_ligada ?g)
        )
    )

    (:action desligar_geladeira
        :parameters (?e - geladeira)
        :precondition (and 
            (geladeira_ligada ?e)
        )
        :effect (and (not (geladeira_ligada ?e)))
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
