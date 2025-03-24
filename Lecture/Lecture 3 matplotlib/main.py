import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
def main():
    print("main() function is being called ... ")

    # plt.style["font.family"] = "monospace" <-- 錯誤寫法! 別跟rcParams搞混了
    plt.style.use("classic")
    plt.rcParams["font.family"] = "monospace"

    x = np.linspace(0.5, 3.5, 100 + 1)
    y = np.sin(x)
    # y1 = np.cos(x)

    # plt.plot(x, y, ".-k", label = 'MyFirstLine') <-- 簡易版
    
    # 如果你被要求客製化很多東西...
    plt.plot(
        x, 
        y,

        # color? 誰的color? 線("--")阿! 不然是誰的?
        color = (1, 0, 1, 0.8), # (R, G, B, A) 
        marker = '^',
        markerfacecolor = 'r', 
        markeredgecolor = 'k',
        markersize = 4,


        linewidth = 2,
        linestyle = "--",
        label=r'$y = \sin(x)$' # r'...': 是告訴compiler '...'裡面的東西是raw string
    )
    
    plt.legend( loc = 1 ) # 要加這一行, 不然不顯示label
    # plt.scatter(x, y1)

    plt.xlim(-5, 5)
    plt.ylim(-1, 1)

    plt.xlabel("x-axis")
    plt.ylabel("y-axis")

    # 顧名思義, 但ls是啥? ... line style!!
    plt.grid(ls = ':', lw = 2)

    plt.axhline(y = 0.4, c = 'r', ls = "--", lw = 2)

    plt.axvspan(xmin = 1.0, xmax = 2, facecolor = 'y', alpha = 0.3)

    # annotate是說我想要給plot出來的圖的某個點做標註, 所以我需要一個點和一段文字
    plt.annotate("maximum",
                 xy = (np.pi/2, 1),
                 xytext = (2, -0.5),
                 weight = 'bold',
                 color = 'r',
                 arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3', color = 'r')
                 )
    
    # what if 我只想要在plot的某個地方放一段文字呢
    plt.text (-2, -0.5, "message from plt.text", weight = 'bold', color = 'b')

    plt.title('structure of matplotlib')
    
    plt.savefig("myfigure.jpg", dpi = 1400, bbox_inches = "tight")





    plt.figure()
    x = ['apple', 'banana', 'orange']
    counts = [20, 30, 10]

    bar_labels = ['red', '_red', 'orange']
    bar_colors = ['tab:red', 'tab:red', 'tab:orange']

    # plt.legend(title = 'Fruit color')
    plt.bar(x, counts, label = bar_labels, color = bar_colors)
    plt.legend(title = 'Fruit color')
    plt.ylabel('Fruit supply')
    plt.title('Fruit supply by kind and color')
    plt.savefig("mybargraph.jpg", dpi = 1400, bbox_inches = 'tight')

    # 有時候就是很機車...tmd好好的柱狀圖不看, 就非得叫你畫那種水平的柱狀圖, 阿一西八 ... 那怎辦?
    # 直接把plt.bar()改成用plt.barh()!
    plt.figure()
    plt.barh(x, counts, label = bar_labels, color = bar_colors)
    plt.legend(title = 'Fruit color')
    plt.ylabel('Fruit supply')
    plt.title('Fruit supply by kind and color')
    plt.savefig('mybarhgraph.jpg', dpi = 1400, bbox_inches = 'tight')

    # 接下來是scatter!
    plt.figure()
    a = np.random.randn(20)
    b = np.random.randn(20)
    plt.scatter(a, b, 
                s = np.power(10*a + 20*b, 2),
                c = a**2 + b**2,
                cmap = mpl.cm.hsv, #我看hsv和binary沒那麼陰間
                marker = 'o')
    plt.savefig('myscattergraph.jpg', dpi = 1400, bbox_inches = 'tight')

if __name__ == "__main__":
    # print(r'\n')
    # print('\n')
    main()



    
