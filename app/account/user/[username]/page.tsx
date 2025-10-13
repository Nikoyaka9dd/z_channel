import Link from "next/link";
import "./style.css" ;
import Image from 'next/image';
import { UserGetData } from '@/types/user';

type Props = {
    params: { username: string }
}

async function fetchUser(username: string): Promise<UserGetData | null> {
    try {
        // 仮想の外部 API からユーザー情報を取得する想定
        const res = await fetch(`https://example.com/api/user/${encodeURIComponent(username)}`, {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
            // サーバーサイド fetch の場合はキャッシュ挙動をコントロールできます
            next: { revalidate: 60 }
        })
        if (!res.ok) return null
        const data: UserGetData = await res.json()
        return data
    } catch (e) {
        console.error('fetchUser error', e)
        return null
    }
}

export default async function Page({ params }: Props){
        const username = params.username
        const data = await fetchUser(username)

        if (!data) {
            return (
                <div className="user-page">
                    <p>ユーザー情報が見つかりませんでした: {username}</p>
                    <Link href="/">ホームへ戻る</Link>
                </div>
            )
        }

        const { user, profile } = data

        return (
            <div className="user-page">
                <div className="user-header">
                    <Image src={user.ico || '/favicon.ico'} alt={user.name} width={64} height={64} />
                    <h2>{user.name}</h2>
                </div>
                <div className="user-intro">
                    <p>{profile.intro}</p>
                </div>
                <div className="user-follow">
                    <h3>フォロー中 ({profile.follow.length})</h3>
                    <ul>
                        {profile.follow.map(f => (
                            <li key={f.id}>{f.name}</li>
                        ))}
                    </ul>
                </div>
            </div>
        )
}