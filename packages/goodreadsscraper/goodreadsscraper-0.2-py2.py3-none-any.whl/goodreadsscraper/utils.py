import sys
import argparse
import json
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from types import SimpleNamespace
from .review import Review

default = True

def prettify_html(page:str)->str:
    soup = BeautifulSoup(page,features='lxml')
    return soup.prettify()


def list_range(l:list,lower_limit:int=None,higher_limit:int=None)->list:
    """Splits the list in a range (special case of only higher or lower limit)"""
    result = l
    if lower_limit and higher_limit:
        if lower_limit > higher_limit:
            return []
        higher_limit = higher_limit - lower_limit

    if lower_limit:
        if lower_limit < len(result):
            result = result[lower_limit:]
        else:
            result = []
    if higher_limit:
        if higher_limit < len(result):
            result = result[:higher_limit]
    return result

def similitarity_percent(string:str,difference:int)->float:
    """Returns the relative difference between the string and the actions number of actions to replicate it"""
    return difference/len(string)


def is_default():
    return default

def get_input(args):
    """Gets the input text according with the register in args"""
    text = ''
    if not args.input:
        for line in sys.stdin:
            text+=line
    else:
        input = args.input
        text = input.read()
    return text

def write_output(out,result):
    """Writes the output on the location registered in args"""
    if not out:
        sys.stdout.write(result)
    else:
        if isinstance(out, tuple):
            out = open(out[0],out[1])
        elif isinstance(out, str):
            out = open(out,"w")
        out.write(result)
        out.close()



def create_dataset(header,list)->pd.DataFrame:
	"""Creates a dataset from a list of already processed into strings of dataset lines"""
	return pd.DataFrame(list,columns=header)


def write_reviews(args,reviews:List[Review],header:bool=False,force:bool=False,delim:str=';'):
    """Writes list of reviews in the given output file"""
    if len(reviews) > 0:
        if args.reviews_output and isinstance(args.reviews_output,str):
            df = create_dataset(reviews[0].header(),[review.dataset_line() for review in reviews])
            if header:
                mode = 'w'
            else:
                mode = 'a'
            df.to_csv(args.reviews_output,sep=delim,columns=reviews[0].header(),quoting=1,mode=mode,index=False,header= header)
        elif force:
            df = create_dataset(reviews[0].header(),[review.dataset_line() for review in reviews])
            if header:
                df.to_csv(sys.stdout,sep=delim,columns=reviews[0].header(),quoting=1,index=False,header = header)
            else:
                df.to_csv(sys.stdout,sep=delim,columns=reviews[0].header(),quoting=1,index=False,header=header)


def costum_csv(list:List[str],header:str=None)->str:
    """Create a costum csv string"""
    csv =''
    if header:
        csv = f'{header}\n'
    for e in list:
        csv+=f'{e}\n'
    return csv

def write_errors(args,errors):
    """Writes the errors on the location registered in args"""
    if not args.errors:
        for e in errors:
            sys.stdout.write(e)
    else:
        file = args.errors[0]
        for e in errors:
            file.write(e)

def log(args,msg):
    """If logging is enabled, prints the log message to stdout"""
    if args.logging:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'LOG : {msg} [{time}]')


def error(args,msg:str):
    """Adds an error message to the error stack"""
    if args.errors:
        args.errors.write(f'Error: {msg}\n')
    else:
	    print(f'Error: {msg}')

def want_reviews(books) -> bool:
    for book in books:
        if(book.reviews_simple or book.reviews):
            return True
    return False  


def process_arguments(args):
    books = []
    authors = []
    invalid = False
    #Apenas um book
    if args.isbn or args.id or args.btitle:
        book = SimpleNamespace(isbn = args.isbn,
                               id = args.id,
                               btitle = args.btitle,
                               author = args.author,
                               output = args.output,
                               logging = args.logging,
                               errors = args.errors,
                               reviews_simple = args.reviews_simple,
                               reviews = args.reviews,
                               reviews_range = args.reviews_range,
                               reviews_language = args.reviews_language,
                               reviews_output = args.reviews_output)

        books.append(book)

    #Apenas um author
    elif args.author:
        author = SimpleNamespace(author = args.author,
                                 maxworks = args.maxworks,
                                 output = args.output,
                                 logging = args.logging,
                                 errors = args.errors,
                                 verbose = args.verbose)

        #author.verbose = args.verbose
        authors.append(author)

    #Json com varios books e varios authors
    elif args.json:
        #Tratar json
        print("FICHEIRO JSON -> ",args.json)
        file = open(args.json[0])
        data = json.load(file)

        if 'books' in data:
            books_json = data['books']
            for book_json in books_json:
                book = SimpleNamespace(isbn = args.isbn,
                               id = args.id,
                               btitle = args.btitle,
                               author = args.author,
                               output = args.output,
                               logging = args.logging,
                               errors = args.errors,
                               reviews_simple = args.reviews_simple,
                               reviews = args.reviews,
                               reviews_range = args.reviews_range,
                               reviews_language = args.reviews_language,
                               reviews_output = None)

                if 'isbn' in book_json:
                    book.isbn = book_json['isbn']
                if 'id' in book_json:
                    book.id = book_json['id']
                if 'name' in book_json:
                    book.btitle = book_json['name']
                if 'author' in book_json:
                    book.author = book_json['author']
                if 'output' in book_json:
                    book.output = book_json['output']
                if 'reviews_simple' in book_json:
                    book.reviews_simple = book_json['reviews_simple']
                if 'reviews' in book_json:
                    book.reviews = book_json['reviews']
                if 'reviews_range' in book_json:
                    if isinstance(book_json['reviews_range'],list) and all([isinstance(item, int) for item in book_json['reviews_range']]) and len(book_json['reviews_range'])==2:
                        book.reviews_range = book_json['reviews_range']
                    else:
                        invalid = True
                if 'reviews_language' in book_json:
                    book.reviews_language = book_json['reviews_language']
                if 'reviews_output' in book_json:
                    book.reviews_output = book_json['reviews_output']

                if not (book.isbn or book.id or book.btitle):
                    invalid = True
                else: 
                    books.append(book)
                if invalid:
                    error(args,f"Error in dic \n {book_json}")
                    break
                

        if 'authors' in data:
            authors_json = data['authors']
            for author_json in authors_json:
                author = SimpleNamespace()
                try:
                    author = SimpleNamespace(author = author_json['name'],
                                 maxworks = args.maxworks,
                                 output = args.output,
                                 logging = args.logging,
                                 errors = args.errors,
                                 verbose = args.verbose)

                    if 'verbose' in author_json:
                        author.verbose = author_json['verbose']
                    if 'mw' in author_json:
                        author.maxworks = author_json['mw']
                    if 'output' in author_json:
                        author.output = author_json['output']
                    authors.append(author)

                except:
                    invalid = True
                if invalid:
                    error(args,f"Error in dic \n {author_json}")
                    break
                    
    if not invalid:
        return books,authors
    else:
        return None


def parse_arguments(__version__)->argparse.Namespace:
    """Process arguments from stdin"""
    parser = argparse.ArgumentParser(
        prog='tok',
        formatter_class=argparse.RawTextHelpFormatter,
        description=f'''
    --------------------------------------------------------------------
                    **BookScraper version {__version__}**
    --------------------------------------------------------------------
                Module to scrap book information from goodreads'''
    )
    parser.add_argument('-isbn'                   ,type=str                        ,nargs='?'  ,default=None                           ,help='isbn of the book to scrape')
    parser.add_argument('-id'                     ,type=str                        ,nargs='?'  ,default=None                           ,help='book id of the book to scrape')
    parser.add_argument('-btitle'                 ,type=str                        ,nargs='?'  ,default=None                           ,help='name of the book to scrape (not precise)')
    parser.add_argument('-a','--author'           ,type=str                        ,nargs='?'  ,default=None                           ,help='author name or id to scrape')
    parser.add_argument('-mw','--maxworks'        ,type=int                        ,nargs='?'  ,default=None                           ,help='maximum number of works to find')
    parser.add_argument('-rs','--reviews_simple'                                                             ,action='store_true'      ,help='gathers reviews of a book (simple mode).\nreviews are written to output as soon as possible to save memory')
    parser.add_argument('-r','--reviews'                                                                     ,action='store_true'      ,help='gathers reviews of a book (full mode, slower)')
    parser.add_argument('-rg','--reviews_range'   ,type=int                        ,nargs=2    ,default=None                           ,help='defines the range of reviews to collect')
    parser.add_argument('-rl','--reviews_language',type=str                        ,nargs='?'  ,default=None                           ,help='defines a language to filter the reviews page')
    parser.add_argument('-ro', '--reviews_output' ,type=str                        ,nargs='?'  ,default=None                           ,help='defines an output file for the reviews dataset')
    parser.add_argument('-o','--output'           ,type=argparse.FileType('w')     ,nargs='?'  ,default=None                           ,help='defines an output file')
    parser.add_argument('-l','--logging'                                                                     ,action='store_true'      ,help='logs the procedure of the program on the stdout')
    parser.add_argument('-j','--json'             ,type=str                        ,nargs=1    ,default=None                           ,help="allows a json file with multiple searches to make to be given")
    parser.add_argument('-e','--errors'           ,type=argparse.FileType('w')     ,nargs=1    ,default=None                           ,help='defines an output file for the errors')
    parser.add_argument('-ve','--verbose'                                                                    ,action='store_true'      ,help='activates verbose outputs')
    parser.add_argument('--version','-V', action='version', version='%(prog)s '+__version__)

    return parser.parse_args()


