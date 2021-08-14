import React from 'react'

const style = {
  display: 'flex',
  flexGrow: 1,
  padding: '5px 0',
  justifyContent: 'space-evenly',
  flexDirection: 'column-reverse'
}

const SentenceList = ({partOfSpeech, children, word}) => {

  return (
    <>
      <div className={partOfSpeech} style={style}>
        {partOfSpeech}
        <div>{word && ' ' + word}</div>
        {children && children.length !== 0 && 
          <div className="children">
            {children.map((item) => (
              <SentenceList key={item.partOfSpeech} {...item} />
            ))}
          </div>
        }
      </div>
    </>
  )
}

export default SentenceList;
