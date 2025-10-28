import Sidebar from "@/components/Sidebar"
import "./style.css";
import mockLabels from '@/types/mock'
import AllZweetScreen from "./main";
import Image from 'next/image';

export default function AllZweetScreeb(){
    // モックデータを挿入
    // 本番環境で要変更
    const { d } = mockLabels;
    return (
        <div className="mainPage">
            <div className="sidebar-loginInfo">
                <Sidebar/>
            </div>
            <div className="mainbar-zweetInfo">
                <div className="logo">
                    <Image
                        src="/img/logo.png" // publicフォルダからのパス
                        alt="Logo"
                        width={600} // 画像の元の幅を指定
                        height={120} // 画像の元の高さを指定
                    />
                </div>
                <div className="center-labels">
                    <AllZweetScreen 
                        d = {d}
                    />
                </div>
            </div>
        </div>
    )
}