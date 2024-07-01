import React from 'react'
import { setStatusBidding } from '../../utils/status-bidding'

import styles from './style.module.css'

export default function CardLicitacoes({ data }) {

  const formatValue = parseFloat(data["Valor_Licitacao"]).toFixed(2)
  const statusBidding = setStatusBidding(data)

  return (
    <div className={styles.cardWrapper}>
      <h5 className={styles.cardTitle}>{data["Nome_UG"]}</h5>
      <div className={styles.cardStatus}>
        <p className={styles.cardStatusText}>Status: {statusBidding}</p>
        <p className={styles.cardStatusText}>{data['tipo']}</p>
      </div>
      <div className={styles.licitacoesInfo}>
        <div className={styles.cardSection}>
          <p>Dara de publicação: {data["data_abertura"]}</p>
          <p>Valor da licitação: {`R$${formatValue}`}</p>
        </div>
        <div>
          <p className={styles.cardDescricao}>{data["Objeto"]}</p>
        </div>
      </div>
      <div>
        <a href="" className={styles.cardButton}>Ver Mais</a>
      </div>
    </div>
  )
}

