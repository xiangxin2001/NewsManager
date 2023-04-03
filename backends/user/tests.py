from django.test import TestCase

# Create your tests here.
import json
import math


def con(rot,cx,cy,x,y):
    resut_x=cx - ((x-cx) * math.cos(rot)) - ((y-cy) * math.sin(rot))
    result_y=cy - ((x-cx) * math.sin(rot))   ((y-cy) * math.cos(rot))
    return resut_x,result_y
#第1问
def rotate(boxs)->dict:
    rotate_box={}
    for i in range(1,len(boxs)+1):
        box=boxs[i]
        top_left_x=box[0][0]
        top_left_y=box[0][1]
        buttom_right_x=box[1][0]
        buttom_right_y=box[1][1]
        rot=box["rot_{}".format(i)]
        mid_point_x=(top_left_x+buttom_right_x)/2
        mid_point_y=(top_left_y+buttom_right_y)/2
        t_l_x,t_l_y=con(rot,mid_point_x,mid_point_y,top_left_x,top_left_y)
        b_r_x,b_r_y=con(rot,mid_point_x,mid_point_y,buttom_right_x,buttom_right_y)
        li=[]
        li.append([t_l_x,t_l_y])
        li.append([b_r_x,t_l_y])
        li.append([b_r_x,b_r_y])
        li.append([t_l_x,b_r_y])
        rotate_box[i]=li
    return rotate_box
#第二问
def perfect_line(boxs,liness):
    perfect_line={}
    for i in range(1,len(boxs)+1):
        box=boxs[i]
        lines=liness[i]
        p_ls=[]
        for line in lines:
            line_x1,line_y1=line[0][0],line[0][1]
            line_x2,line_y2=line[1][0],line[1][1]
            m=(line_y2-line_y1)/(line_x2-line_x1)
            a=0.0
            b=0.0
            l=0.0
            y1=m*box[0][0]
            y2=m*box[1][0]
            x1=box[0][1]/m
            x2=box[2][1]/m
            if box[0][0]<=x1<=box[1][0]:
                a=x1
            elif box[0][0]<=x2<=box[1][0]:
                a=x2
            if box[0][1]<=y1<=box[2][1]:
                b=y1
            elif box[0][1]<=y2<=box[2][1]:
                b=y2
            if a!=0.0 and b!=0.0:
                if line_x1<=a<=line_x2:
                    ay=a*m
                    if line_y1>b:
                        l=pow((pow((a-line_x1),2)+pow((line_y1-ay),2)),0.5)
                    elif line_y1<=b<=line_y2:
                        l=pow((pow((a-bx),2)+pow((b-ay),2)),0.5)
                    else:
                        l=pow((pow((a-line_x2),2)+pow((line_y2-ay),2)),0.5)
                elif line_x1>a:
                    bx=b/m
                    if line_y1<=b<=line_y2:
                        l=pow((pow((line_x1-bx),2)+pow((line_y1-b),2)),0.5)
                else:
                    bx=b/m
                    if line_y1<=b<=line_y2:
                        l=pow((pow((line_x2-bx),2)+pow((line_y2-b),2)),0.5)
            else:
                l=0
            if l>30:
                p_ls.append([[line_x1,line_y1],[line_x2,line_y2]])
        perfect_line[i]=p_ls

    return perfect_line

#第三问
def jiaodian(rotate_box,perfect_line):
    result=[]
    for i in range(1,len(rotate_box)+1):
        box=rotate_box[i]
        lines=perfect_line[i]
        p_ls=[]
        for line in lines:
            line_x1,line_y1=line[0][0],line[0][1]
            line_x2,line_y2=line[1][0],line[1][1]
            m=(line_y2-line_y1)/(line_x2-line_x1)
            a=0.0
            b=0.0
            l=0.0
            y1=m*box[0][0]
            y2=m*box[1][0]
            x1=box[0][1]/m
            x2=box[2][1]/m
            if box[0][0]<=x1<=box[1][0]:
                a=x1
            elif box[0][0]<=x2<=box[1][0]:
                a=x2
            if box[0][1]<=y1<=box[2][1]:
                b=y1
            elif box[0][1]<=y2<=box[2][1]:
                b=y2
            p_ls.append([[a,a*m],[b/m,b]])
    result.append(p_ls)

    return result
if __name__=='__main__':
    data=input()
    box_line=json.loads(data)
    boxs=box_line["box"]
    lines=box_line["line"]
    a=rotate(boxs)
    b=perfect_line(boxs,lines)
    jiaodian(a,b)