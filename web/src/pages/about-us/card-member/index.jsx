import styles from './style.module.css'
import { FaGithub } from "react-icons/fa";

export default function CardMember({nome, descricao, github, id}){

    return(
        <div 
         className={styles.cardAboutUsContext}
         style={{flexDirection: (id%2 === 1 ? 'row' : 'row-reverse')}}>
            <span>
                <h3 className={styles.cardAboutUsNome}>{nome}</h3>
                <p className={styles.cardAboutUsDes}>{descricao}</p>
            </span>
            <span className={styles.cardAboutUsPhotoContext}>
                <img className={styles.cardAboutUsPhoto} src={`../../../../assets/members/${id}.jpg`} alt='Foto do membro'/>
                <a href={github} target='blank'>
                    <FaGithub/> Github
                </a>
            </span>
        </div>
    )
}