import React from 'react'

const SentenceList = ({partOfSpeech, children, word}) => {
  return (
    <ul>
      <li>{partOfSpeech}{word && ': ' + word} 
        {children && children.map((item) => (
          <SentenceList key={item.partOfSpeech} {...item} />
        ))}
      </li>
    </ul>
  )
}

export default SentenceList;
