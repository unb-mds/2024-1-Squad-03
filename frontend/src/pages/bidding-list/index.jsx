import React, { useEffect, useState } from 'react'
import Header from '../../components/header'
import Filter from './filter'
import CardLicitacoes from '../../components/card-licitacoes';
import search from '../../../assets/SearchDark.svg';
import styles from './style.module.css'
import { getLicitacoes, pagLicitacoes } from '../../services/licitacoes.service';


export default function BiddingList() {

  const licitacoes = getLicitacoes();
  const [listaLicitacoes, setListaLicitacoes] = useState([]);

  useEffect(() => {
    setListaLicitacoes(pagLicitacoes(licitacoes, 10, 0));
  }, [])
  return (
    <>
      <Header />
      <section className={styles.mainSection}>
        <div className={styles.campoPesquisaWrapper} >
          <div className={styles.campoPesquisa}>
            <img src={search} className={styles.searchIcon} alt="" />
            <input type="text" placeholder='Busque por uma licitação' className={styles.inputStyle} />
          </div>
          <div>
            <div>
              <a href="" className={styles.botaoBuscar}>Buscar</a>
            </div>
          </div>
        </div>
        <div className={styles.licitacoesSection}>
          <Filter />
          <div className={styles.cardsWrapper}>
            {listaLicitacoes.map(item => {
              return (
                <CardLicitacoes data={item}/>
              );
            })}
          </div>
        </div>
      </section>
    </>
  )
}
