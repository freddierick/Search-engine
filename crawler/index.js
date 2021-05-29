const input = "where is the moon?";

function tokenization(text){
    a = text.split(" "); //split
    a = a.map(e => e.toLowerCase()); //lower case 
    return a;
};

console.log(tokenization(input));