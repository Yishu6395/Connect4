import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
#from time import time

class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time 
        
    def opponent_number(self):
        """ changes the turn of the player by passing the turn to the opponent """
        if(self.player_number==1):
            return 2
        else:
            return 1
        
    def revert_changes(self,state,move,pl_num):
        n,m= state[0].shape
        board=state[0]
        dic=state[1]
        if(move[1]):
            for i in range(0,n-1):
                board[i][move[0]]=board[i+1][move[0]]
            board[n-1][move[0]]=move[2]
            dic[pl_num].increment()
            #print("Incrementing")
            #print(dic[pl_num])
        else:
            for i in range(n):
                if(board[i][move[0]]!=0):
                    board[i][move[0]]=0
                    break
        
    def apply_changes(self,board :np.array,dic:Dict[int,Integer],move:Tuple[int,bool],pl_num)->Tuple[np.array,Dict[int,Integer]]:
        if(move[1]):
            #print(move)
            #print(dic[pl_num].get_int())
            #print(get_valid_actions(pl_num,(board,dic)))
            for i in reversed(range(1,board.shape[0])):
                board[i][move[0]]=board[i-1][move[0]]
            board[0][move[0]]=0
            dic[pl_num].decrement()
            #print("Decrementing")
            #print(dic[pl_num])
        else:
            #print(move)
            #print(dic[pl_num].get_int())
            #print(get_valid_actions(pl_num,(board,dic)))
            for i in range(board.shape[0]):
                if(board[i][move[0]]!=0):
                    board[i-1][move[0]]=pl_num
                    break
                if(i==board.shape[0]-1):
                    board[i][move[0]]=pl_num
                
    
    
    def evaluation_score(self,state: Tuple[np.array,Dict[int,Integer]]):
        a=self.player_number
        b=self.opponent_number()
        scorea=get_pts(a,state[0])
        scoreb=get_pts(b,state[0])
        pop_movesa=state[1][a].get_int()
        pop_movesb=state[1][b].get_int()
        wt_score= 1
        wt_pop_move=3.5
        
        return wt_score*(scorea-scoreb)+wt_pop_move*(pop_movesa-pop_movesb)
    
    
    def min_intelligent(self,state: Tuple[np.array,Dict[int,Integer]] , count,alpha,beta):
        if(count<=0):
            return (self.evaluation_score(state),-1)
        else:
            actions =get_valid_actions(self.opponent_number(),state)
            if(len(actions)==0):
                return (self.evaluation_score(state),-1)
            else:
                v=np.inf
                move='a'
                for i in range(len(actions)):
                    if(actions[i][1]):
                        mv=(actions[i][0],actions[i][1],state[0][state[0].shape[0]-1][actions[i][0]])
                    else:
                        mv=(actions[i][0],actions[i][1],-1)
                    
                    self.apply_changes(state[0],state[1],actions[i],self.opponent_number())
                    
                    k=self.max_intelligent(state,count-1,alpha,beta)
                    
                    self.revert_changes(state, mv, self.opponent_number())
                    
                    if(k[0]<v):
                        move=i
                        v=k[0]
                    if(v<=alpha):
                        return (v,move)
                    beta=min(beta,v)
                return (v,move)
    
    def max_intelligent(self,state: Tuple[np.array,Dict[int,Integer]] , count,alpha,beta):
        
        if(count<=0):
            return (self.evaluation_score(state),-1)
        else:
            actions =get_valid_actions(self.player_number,state)
            if(len(actions)==0):
                return (self.evaluation_score(state),-1)
            else:
                v=-np.inf
                move='a'
                for i in range(len(actions)):
                    if(actions[i][1]):
                        mv=(actions[i][0],actions[i][1],state[0][state[0].shape[0]-1][actions[i][0]])
                    else:
                        mv=(actions[i][0],actions[i][1],self.player_number)
                        
                    self.apply_changes(state[0],state[1],actions[i],self.player_number)
                    
                    k=self.min_intelligent(state,count-1,alpha,beta)
                    
                    self.revert_changes(state, mv, self.player_number)
                    
                    if(k[0]>v):
                        move=i
                        v=k[0]
                    if(v>=beta):
                        return (v,move)
                    alpha=max(alpha,v)
                return (v,move)
                    

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """  
        #print("Player "+str(self.player_number)+"making move.")
        #st=time()
        actions=get_valid_actions(self.player_number,state)
        if(len(actions)<=8):
                if(self.time > 15):
                    n = 7
                else:
                    n = 6
        elif(self.time>15 and 9<=len(actions)<13):
            n=5
        elif(self.time < 10 and len(actions) >= 13):
            n = 3
        else: 
            n=4
        k=self.max_intelligent(state,n,-np.inf,np.inf)
        #et=time() 
        #print(et-st)
        return actions[k[1]]
  
        raise NotImplementedError('Whoops I don\'t know what to do')
     
    def exp_expectimax(self,state: Tuple[np.array,Dict[int,Integer]] , count,pl_num):
        if(count==0):
            return (self.evaluation_score(state))
        else:
            actions =get_valid_actions(pl_num,state)
            if(len(actions)==0):
                return (self.evaluation_score(state))
            else:
                v=0
                for i in range(len(actions)):
                    if(actions[i][1]):
                        mv=(actions[i][0],actions[i][1],state[0][state[0].shape[0]-1][actions[i][0]])
                    else:
                        mv=(actions[i][0],actions[i][1],self.opponent_number())
                    
                    self.apply_changes(state[0],state[1],actions[i],pl_num)
                    
                    if(pl_num==self.player_number):
                        k=self.exp_expectimax(state,count-1,self.opponent_number())
                    else:
                        k=self.exp_expectimax(state,count-1,self.player_number)
                    
                    self.revert_changes(state, mv, pl_num)
                    
                    v+=k
                
                return v/len(actions)
    
    def max_expectimax(self,state: Tuple[np.array,Dict[int,Integer]] , count):
        
        if(count==0):
            return (self.evaluation_score(state),-1)
        else:
            actions =get_valid_actions(self.player_number,state)
            if(len(actions)==0):
                return (self.evaluation_score(state),-1)
            else:
                v=-np.inf
                move='a'
                for i in range(len(actions)):
                    if(actions[i][1]):
                        mv=(actions[i][0],actions[i][1],state[0][state[0].shape[0]-1][actions[i][0]])
                    else:
                        mv=(actions[i][0],actions[i][1],self.player_number)
                        
                    self.apply_changes(state[0],state[1],actions[i],self.player_number)
                    
                    k=self.exp_expectimax(state,count-1,self.opponent_number())
                    
                    self.revert_changes(state, mv, self.player_number)
                    
                    if(k>v):
                        move=i
                        v=k
                return (v,move)

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """ 
        

        actions=get_valid_actions(self.player_number,state)
        if(self.time==20 and 9<=len(actions)<13):
            n=4
        elif(self.time==20 and len(actions)<=8):
            n=5
        elif(len(actions)<8):
            n=4
        else:
            n=3
        
        st=time()
        k=self.max_expectimax(state,n)
        et=time()
        return actions[k[1]]
        raise NotImplementedError('Whoops I don\'t know what to do')

